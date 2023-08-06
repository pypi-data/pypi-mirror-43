from shiftmemory import exceptions, adapter


class Memory():
    """
    Main memory API
    Keeps track of caches, configures and instantiates them on demand and
    provides means to perform operations on caches
    """

    def __init__(self, *args, **kwargs):
        """
        Creates your memory instance
        Give it your caches configuration as a dictionary
        """
        self.adapters = dict()
        self.caches = dict()
        self._cache_instances = dict()
        self.config = dict(adapters=dict(), caches=dict())

        if args or kwargs:
            self.init(*args, **kwargs)

    def init(self, adapters=None, caches=None):
        """
        Delayed initializer
        This can be called by __init__ or later.

        :param adapters: dict, adapters configuration
        :param caches: dict, caches configuration
        :return:
        """
        if adapters:
            self.adapters = adapters
        if caches:
            self.caches = caches

    def get_cache(self, cache_name):
        """
        Get cache
        Checks if a cache was already created and returns that. Otherwise
        attempts to create a cache from configuration and preserve
        for future use
        """
        if cache_name in self._cache_instances:
            return self._cache_instances[cache_name]

        if cache_name not in self.caches:
            error = 'Cache [{}] is not configured'.format(cache_name)
            raise exceptions.ConfigurationException(error)

        cache_config = self.caches[cache_name]
        adapter_name = cache_config['adapter']

        if adapter_name not in self.adapters:
            error = 'Adapter [{}] is not configured'.format(adapter_name)
            raise exceptions.ConfigurationException(error)

        adapter_config = self.adapters[adapter_name]
        adapter_type = adapter_config['type']
        adapter_class = adapter_type[0].upper() + adapter_type[1:]

        if not hasattr(adapter, adapter_class):
            error = 'Adapter class [{}] is missing'.format(adapter_class)
            raise exceptions.AdapterMissingException(error)

        cls = getattr(adapter, adapter_class)
        adapter_params = dict(
            namespace=cache_name,
            ttl=cache_config['ttl'],
        )
        if 'config' in adapter_config:
            adapter_params['config'] = adapter_config['config']

        cache = cls(**adapter_params)
        self._cache_instances[cache_name] = cache
        return self._cache_instances[cache_name]

    def drop_cache(self, name):
        """
        Drop cache
        Deletes all items in cache by name
        """
        cache = self.get_cache(name)
        if not hasattr(cache, 'delete_all'):
            cls = type(cache)
            error = 'Adapter [{}] can not drop cache by namespace'.format(cls)
            raise exceptions.AdapterFeatureMissingException(error)

        return cache.delete_all()

    def drop_all_caches(self):
        """
        Drop all caches
        Goes through every configured cache and drops all items. Will
        skip certain caches if they do not support drop all feature
        """
        for name in self.caches.keys():
            cache = self.get_cache(name)
            if hasattr(cache, 'delete_all'):
                cache.delete_all(name)
        return True

    def optimize_cache(self, name):
        """
        Optimize cache
        Gets cache by name and performs optimization if supported
        """
        cache = self.get_cache(name)
        if not hasattr(cache, 'optimize'):
            cls = type(cache)
            error = 'Adapter [{}] can not optimize itself'.format(cls)
            raise exceptions.AdapterFeatureMissingException(error)

        return cache.optimize()

    def optimize_all_caches(self):
        """
        Optimize all caches
        Goes through every configured cache and optimizes. Will
        skip certain caches if they do not support optimization feature
        """
        for name in self.caches.keys():
            cache = self.get_cache(name)
            if hasattr(cache, 'optimize'):
                cache.optimize(name)
        return True






