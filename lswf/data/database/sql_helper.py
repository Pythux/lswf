from lswf.service.init import sql


class SQLHelper:
    def _create(self, values_names, values):
        values_interog = ', '.join(['?'] * len(values_names))
        return sql(
            'insert into {}({}) values ({})'
            .format(self.table, ', '.join(values_names), values_interog),
            *values)

    def _read(self, key, values_names, values):
        if key:
            where = self.key_name + ' = ?', (key,)
        elif isinstance(values_names, list):
            where = (' AND '.join([name + ' = ?' for name in values_names]),
                     values)
        else:
            where = values_names + ' = ?', (values,)

        r = sql(
            'select * from {} where {}'
            .format(self.table, where[0]),
            *where[1])

        if r == []:
            return None
        elif len(r) != 1:
            raise ValueError('_read must return a single element')
        else:
            return r[0]

    def _update(self, key, values_names, values):
        if not key:
            raise ValueError("can't update without the obj key")

        if not isinstance(values_names, list):
            values_names = [values_names]

        values_names = ', '.join([name + ' = ?' for name in values_names])
        sql('update {} set {} where {} = ?'
            .format(self.table, values_names, self.key_name),
            *values, key)

    def _delete(self, obj):
        if not obj.key:
            raise ValueError("can't delete without the obj key")
        sql('delete from {} where {} = ?'
            .format(self.table, self.key_name),
            obj.key)
        obj.key = None
