from enum import Enum

class Category(Enum):
    RANSOMWARE = 'Ransomware'
    DDOS = 'DDoS Attack'
    MALWARE = 'Malware'
    PHISHING = 'Phishing'
    DATA_LEAK = 'Data Leak'
    COMBO_LIST = 'Combo List'
    DATA_BREACH = 'Data Breach'
    LOGS = 'Logs'
    DEFACEMENT = 'Defacement'
    ALERT = 'Alert'
    VULNERABILITY = 'Vulnerability'
