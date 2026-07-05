import os


def build_dashboard_html(devices, action_devices, path="output/dashboard.html"):
    os.makedirs(os.path.dirname(path), exist_ok=True)

    action_map = {
        d["ip"]: d["actions_checked"]
        for d in action_devices
    }

    rows = ""

    for device in devices:
        actions = action_map.get(device["ip"], "No Supported Actions")

        rows += f"""
        <tr>
            <td>{device['hostname']}</td>
            <td>{device['ip']}</td>
            <td>{device['mac']}</td>
            <td>{device['health']}</td>
            <td>{device['ports']}</td>
            <td>{device['type']}</td>
            <td>{actions}</td>
        </tr>
        """

    html = f"""
    <html>
    <head>
        <title>DON Dashboard</title>
        <style>
            body {{
                font-family: Arial;
                background: #111;
                color: #eee;
                padding: 20px;
            }}
            h1 {{
                color: #4ade80;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                background: #1e1e1e;
            }}
            th, td {{
                border: 1px solid #333;
                padding: 10px;
                text-align: left;
            }}
            th {{
                background: #222;
                color: #4ade80;
            }}
            tr:hover {{
                background: #2a2a2a;
            }}
        </style>
    </head>
    <body>
        <h1>DON Dashboard</h1>

        <p>Devices discovered on your network.</p>

        <table>
            <tr>
                <th>Hostname</th>
                <th>IP</th>
                <th>MAC</th>
                <th>Health</th>
                <th>Open Ports</th>
                <th>Device Type</th>
                <th>Compatible Actions</th>
            </tr>
            {rows}
        </table>
    </body>
    </html>
    """

    with open(path, "w", encoding="utf-8") as file:
        file.write(html)