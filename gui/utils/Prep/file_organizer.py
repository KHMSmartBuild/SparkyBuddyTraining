import os
import sys
import file_management as fm
import file_conversion as fc
import preprocessing as pp
import save_data as sd
import ConversationLoader as cl
from data.raw_data.tools import append_to_csv, data_collection, data_preprocessing, data_splitting, raw_text_prep
from data.raw_data.tools import Audio_Trans_clean, pdf_reader, data_scraper

class FileOrganizer:
    def __init__(self, path):
        self.path = path
    
    def organize_files(self):
        # Code to organize files in the specified path
        organized_files = fm.organize_files(self.path)
        return organized_files
    
class DataConverter:
    def __init__(self, data):
        self.data = data
        
    def convert_data(self, input_format, output_format):
        # Code to convert data to a specified format
        converted_data = fc.convert_data(self.data, input_format, output_format)
        return converted_data
    
class DataPreprocessor:
    def __init__(self, data):
        self.data = data
        
    def preprocess_data(self):
        # Code to preprocess data
        preprocessed_data = pp.preprocess_data(self.data)
        return preprocessed_data
