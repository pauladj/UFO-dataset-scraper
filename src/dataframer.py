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
