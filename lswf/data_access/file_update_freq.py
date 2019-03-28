from .update_frequence import SQL as UpdateFrequence


class FileUpdateFrequence(UpdateFrequence):
    @property
    def table(self):
        return 'file_update_frequence'

    fk_name = 'file_id'

    # @property
    # def key_name(self):
    #     return 'file_id'
