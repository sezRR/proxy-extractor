import os


class BusinessRule:
    @staticmethod
    def write_data_file_need_to_be_does_not_exist_to_write(write_data_file_path: str) -> bool:
        if os.path.exists(write_data_file_path):
            print("Destination file was already created.")
            return False

        return True
