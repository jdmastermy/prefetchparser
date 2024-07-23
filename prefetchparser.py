import os
import struct
import pandas as pd
from datetime import datetime, timedelta

def parse_prefetch(filename):
    with open(filename, 'rb') as f:
        header = f.read(84)
        if len(header) < 84:
            return None

        magic, version, file_size, _ = struct.unpack('<4sI12xI48x4x', header[:64])
        if magic != b'SCCA':
            return None

        # Parse basic information
        executable_name = os.path.basename(filename)
        run_count, last_run_time = struct.unpack('<I16xQ', header[16:40])

        last_run_time = convert_windows_timestamp(last_run_time)

        # Extract volume information
        f.seek(84)
        volume_info_offset, volume_info_size, _ = struct.unpack('<I4xI4xI', f.read(20))
        f.seek(volume_info_offset)
        volume_data = f.read(volume_info_size)
        volume_creation_time, = struct.unpack('<Q', volume_data[:8])
        volume_creation_time = convert_windows_timestamp(volume_creation_time)
        file_reference, = struct.unpack('<Q', volume_data[8:16])
        volume_serial_number, = struct.unpack('<I', volume_data[16:20])

        # Extract accessed files list
        file_list_offset, file_list_size = struct.unpack('<II', volume_data[20:28])
        f.seek(file_list_offset)
        file_list_data = f.read(file_list_size)
        file_list = parse_accessed_files(file_list_data)

        file_info = {
            'Executable Name': executable_name,
            'Run Count': run_count,
            'Last Run Time': last_run_time,
            'Volume Creation Time': volume_creation_time,
            'File Reference': file_reference,
            'Volume Serial Number': volume_serial_number,
            'Accessed Files': file_list
        }

        return file_info

def convert_windows_timestamp(timestamp):
    dt = datetime(1601, 1, 1) + timedelta(microseconds=timestamp // 10)
    return dt.strftime('%Y-%m-%d %H:%M:%S')

def parse_accessed_files(data):
    files = []
    while data:
        file_length, = struct.unpack('<I', data[:4])
        file_name = data[4:4 + file_length].decode('utf-16le', errors='ignore').strip('\x00')
        files.append(file_name)
        data = data[4 + file_length:]
    return files

def process_prefetch_files(input_folder, output_folder):
    prefetch_files = [f for f in os.listdir(input_folder) if f.endswith('.pf')]
    prefetch_data = []

    for prefetch_file in prefetch_files:
        file_path = os.path.join(input_folder, prefetch_file)
        file_info = parse_prefetch(file_path)
        if file_info:
            prefetch_data.append(file_info)

    df = pd.DataFrame(prefetch_data)
    output_file = os.path.join(output_folder, 'prefetch_data.csv')
    df.to_csv(output_file, index=False)
    print(f'Prefetch data has been saved to {output_file}')

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Parse Windows Prefetch artifacts and output to CSV.')
    parser.add_argument('input_folder', type=str, help='The input folder containing prefetch files.')
    parser.add_argument('output_folder', type=str, help='The output folder to save the CSV file.')
    args = parser.parse_args()

    process_prefetch_files(args.input_folder, args.output_folder)
