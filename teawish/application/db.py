class IUoW:
    async def commit(self): ...

    async def rollback(self): ...

    async def flush(self): ...
