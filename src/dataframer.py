import pandas as pd


class DataFramer:

    @staticmethod
    def initialize_dataframe(header):
        """
        Create an empty dataframe
        :param header: names of the columns
        :return: dataframe
        """
        df = pd.DataFrame(columns=header)
        return df

    @staticmethod
    def append_to(dataframe, row):
        """
        Apend a row to an existing dataframe
        :param row: an array with the info of one row
        :return: the dataframe with the row appended
        """
        new_dataframe = pd.DataFrame([row], columns=dataframe.columns)
        dataframe = dataframe.append(new_dataframe)
        return dataframe

    @staticmethod
    def export_to_csv(dataframe, output_file):
        """
        Export a dataframe to a csv
        :param dataframe: dataframe to export
        :param output_file: the output file
        """
        try:
            dataframe.to_csv(output_file, index=False, encoding="cp1252")
        except Exception as e:
            raise Exception("Error saving the file: {}".format(str(e)))
