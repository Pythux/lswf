from .update_frequence import SQL as UpdateFrequence


class DirectoryUpdateFrequence(UpdateFrequence):
    @property
    def table(self):
        return 'directory_update_frequence'

    # @property
    # def key_name(self):
    #     return 'directory_id'

    fk_name = 'directory_id'
