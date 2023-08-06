import ledis
from seneca.libs.logger import get_logger
from seneca.engine.conflict_resolution import CRDataGetSet, CRContext, CRDataBase, CR_EXCLUDED_KEYS


class CRCmdMeta(type):
    def __new__(cls, clsname, bases, clsdict):
        clsobj = super().__new__(cls, clsname, bases, clsdict)
        if not hasattr(clsobj, 'registry'):
            clsobj.registry = {}

        if 'COMMAND_NAME' in clsdict:
            cmd_name = clsdict['COMMAND_NAME']
            assert cmd_name not in clsobj.registry, "Command {} already in registry {}".format(cmd_name, clsobj.registry)
            clsobj.registry[cmd_name] = clsobj

        return clsobj


class CRCmdBase(metaclass=CRCmdMeta):
    DATA_NAME = None

    # TODO -- remove the finalize var. We dont need this.
    def __init__(self, working_db, master_db, sbb_idx: int, contract_idx: int, data: CRContext):
        self.log = get_logger("{}[sbb_{}][contract_{}]".format(type(self).__name__, sbb_idx, contract_idx))
        self.data = data
        self.working, self.master = working_db, master_db
        self.sbb_idx, self.contract_idx = sbb_idx, contract_idx

    def set_params(self, working_db, master_db, sbb_idx: int, contract_idx: int, data: CRContext):
        self.data = data
        self.working, self.master = working_db, master_db
        self.sbb_idx, self.contract_idx = sbb_idx, contract_idx

    def _copy_og_key_if_not_exists(self, key, *args, **kwargs):
        """
        Copies the key from either master db or common layer (working db) to the sub-block specific layer, if it does
        not exist already
        """

        # debug
        # self.log.info("key {} and master is {}".format(key, self.master))
        # self.log.notice("master has keys:\n{}".format(self.master.keys()))
        # end debug

        # If the key already exists, bounce out of this method immediately
        if self._sbb_original_exists(key, *args, **kwargs):
            self.log.spam("Key <{}> already exists in sub-block specific data, thus not recopying".format(key))
            return

        # First check the common layer for the key
        if self._db_original_exists(self.working, key, *args, **kwargs):
            self.log.spam("Copying common key <{}> to sb specific data" .format(key))
            self._copy_key_to_sbb_data(self.working, key, *args, **kwargs)

        # Next, check the Master layer for the key
        elif self._db_original_exists(self.master, key, *args, **kwargs):
            self.log.spam("Copying master key <{}> to sb specific data" .format(key))
            self._copy_key_to_sbb_data(self.master, key, *args, **kwargs)

        # Otherwise, if key not found in common or master layer, mark the original as None
        else:
            self.log.spam("Key {} not found in master layer. Defaulting original to None.".format(key))
            self._copy_key_to_sbb_data(None, key, *args, **kwargs)

    def _add_key_to_redo_log(self, key, *args, **kwargs):
        raise NotImplementedError()

    def __call__(self, *args, **kwargs):
        raise NotImplementedError()

    def _db_original_exists(self, db, key, *args, **kwargs) -> bool:
        """
        Returns True if 'key' exists on db. False otherwise. args/kwargs can be supplied for more complex
        implementations by subclasses
        :param db: The DB to check
        :param key: The key to check on 'db'
        """
        raise NotImplementedError()

    def _sbb_original_exists(self, key, *args, **kwargs) -> bool:
        """
        Return True if key exists in the sub-block specific data, and False otherwise.
        """
        raise NotImplementedError()

    def _copy_key_to_sbb_data(self, db, key, *args, **kwargs):
        """
        Copies 'key' from the specified to the sub-block specific data
        :param db: The DB to copy the key from. If None, it is implied that the key does not exist in common/master, and
        thus the original value will be set as None
        :param key: The name of the key to copy
        """
        raise NotImplementedError()


class CRCmdExists(CRCmdBase):
    COMMAND_NAME = 'exists'

    def __call__(self, key):
        # TODO do we need to add book keeping information on this
        # TODO this could be made more modular. Current implementation will not scale well --davis
        # First check if key exists in getset
        if key in self.data['getset']:
            return True
        # Then check if it exists in the common layer...
        if self.working.exists(key):
            return True
        # Then finally, check if it exists in the master layer
        return self.master.exists(key)


class CRCmdGetSetBase(CRCmdBase):
    DATA_NAME = 'getset'

    def _db_original_exists(self, db, key) -> bool:
        return db.exists(key)

    def _sbb_original_exists(self, key) -> bool:
        return key in self.data['getset']

    def _copy_key_to_sbb_data(self, db, key):
        val = db.get(key) if db else None
        self.data['getset'][key] = {'og': val, 'mod': None, 'contracts': set()}

    def _get(self, key, return_none=True):
        self._copy_og_key_if_not_exists(key)

        # TODO make all this DRYer so you can abstract it like a pro

        # First, try and return the local modified key
        val = self.data['getset'][key]['mod']
        if val is not None:
            self.log.spam("SBB specific MODIFIED key found for key named <{}>".format(key))
        # Otherwise, default to the local original key
        else:
            self.log.spam("SBB specific ORIGINAL key found for key named <{}>".format(key))
            val = self.data['getset'][key]['og']

        if val is None and not return_none:
            raise Exception("Key '{}' does not exist, but was attempted to be GET".format(key))

        # TODO properly handle CR on stamps key
        if key not in CR_EXCLUDED_KEYS:
            self.data['getset'].reads[self.contract_idx].add(key)
            self.data['getset'][key]['contracts'].add(self.contract_idx)

        return val


# TODO refactor this so they can live in the same base class, and we just specify the command name with a decorator
class CRCmdGet(CRCmdGetSetBase):
    COMMAND_NAME = 'get'

    def __call__(self, key):
        return self._get(key)


class CRCmdSet(CRCmdGetSetBase):
    COMMAND_NAME = 'set'

    def _add_key_to_redo_log(self, key, *args, **kwargs):
        # Return if key already exist in this contract's redo log
        if key in self.data['getset'].redo_log[self.contract_idx]:
            return

        self.data['getset'].redo_log[self.contract_idx][key] = self._get(key, return_none=True)
        self.log.spam("Contract {} added key {} to redo log with val {}".format(self.contract_idx, key,
                                                                                self.data['getset'].redo_log[
                                                                                self.contract_idx][key]))

    def __call__(self, key, value):
        # TODO properly handle CR on stamps key
        if key in CR_EXCLUDED_KEYS:
            return

        assert type(value) in (str, bytes), "Attempted to use 'set' with a value that is not str or bytes (val={}). " \
                                            "This is not supported currently.".format(value)
        self._copy_og_key_if_not_exists(key)
        if type(value) is str:
            value = value.encode()

        self._add_key_to_redo_log(key)

        self.log.spam("Setting SBB specific key <{}> to value {}".format(key, value))
        self.data['getset'][key]['mod'] = value
        self.data['getset'][key]['contracts'].add(self.contract_idx)
        self.data['getset'].writes[self.contract_idx].add(key)
        self.data['getset'].outputs[self.contract_idx] += 'SET {} {};'.format(key, value.decode())


class CRCmdHGet(CRCmdGet):
    COMMAND_NAME = 'hget'

    def __call__(self, key, field):
        prefixed_key = "{}:{}".format(key, field)
        return super().__call__(prefixed_key)



class CRCmdHSet(CRCmdSet):
    COMMAND_NAME = 'hset'

    def __call__(self, key, field, value):
        prefixed_key = "{}:{}".format(key, field)
        return super().__call__(prefixed_key, value)

