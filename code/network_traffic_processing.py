import os
import subprocess
import cicflowmeter
from scapy.all import sniff, wrpcap
from datetime import datetime
import feature_mapping
import pandas as pd

now = datetime.now()
formatted_date_time = now.strftime("%Y-%m-%d_%H-%M-%S")

def capture_traffic():
    save_to_dir = 'pcap/' + formatted_date_time + '.pcap'
    packets = sniff(count=10)
    wrpcap(save_to_dir, packets)

def pcap_to_csv(pcap_file, csv_output):
    try:
        command = ['cicflowmeter', '-f', pcap_file, '-c', csv_output]
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("Command executed successfully!")
        print(result.stdout.decode())

    except subprocess.CalledProcessError as e:
        print("Error executing command:")
        print(e.stderr.decode())

def field_mapping():
    # preprocessing file to field mapping
    pcap_path = './pcap'
    for pcap_file in os.listdir(pcap_path):
        full_file_path = os.path.join(pcap_path, pcap_file)
        print('Processing file:', full_file_path)
        if pcap_file.endswith('.pcap'):
            csv_file_name = pcap_file.replace('.pcap', '.csv')
            csv_file_path = os.path.join('generated_csv', csv_file_name)
            if not os.path.exists('generated_csv'):
                os.makedirs('generated_csv')
            pcap_to_csv(full_file_path, csv_file_path)

    csv_path = './generated_csv'
    for csv_file in os.listdir(csv_path):
        file_path = os.path.join(csv_path, csv_file)
        try:
            data = pd.read_csv(file_path)
            missing_columns = [col for col in feature_mapping.mapping_dict if col not in data.columns]
            if missing_columns:
                print(f"Warning: Columns {missing_columns} not found in {csv_file}. Skipping.")
                continue
            data.rename(columns=feature_mapping.mapping_dict, inplace=True)
            names_to_drop = ['src_ip',
                            'dst_ip',
                            'src_port',
                            'protocol',
                            'timestamp']
            data.drop(columns=names_to_drop, inplace=True)
            data.to_csv(file_path, index=False)
            print(f"Processed {csv_file} successfully.")
        except pd.errors.EmptyDataError:
            print(f"Warning: {csv_file} is empty. Skipping.")
        except Exception as e:
            print(f"Error processing {csv_file}: {e}")
