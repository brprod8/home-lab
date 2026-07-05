# DON - Devices On Network

A lightweight home network discovery tool.

DON scans a subnet, finds online devices, pulls MAC addresses, attempts hostname lookup with nslookup, checks common ports, adds device intelligence, checks basic network health, and exports everything to CSV.

## Run

```powershell
cd DON
python main.py
```

## Change subnet

Open `don/config.py` and change:

```python
SUBNET = "192.168.20"
```

For guest network:

```python
SUBNET = "192.168.20"
```

## Output

Results save to:

```text
output/don_table.csv
```
