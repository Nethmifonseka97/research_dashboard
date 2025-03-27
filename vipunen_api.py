import requests
import pandas as pd

class VipunenAPI:
    def __init__(self, caller_id="your_organization_id"):
        self.base_url = "https://api.vipunen.fi/api/resources"
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Caller-Id": caller_id
        }

    def fetch_data(self, dataset, filters=None, limit=5000):
        data = []
        offset = 0
        has_more_data = True

        # Build initial API endpoint
        filter_query = f"&filter={filters}" if filters else ""
        count_url = f"{self.base_url}/{dataset}/data/count?{filter_query}"

        try:
            response = requests.get(count_url, headers=self.headers)
            print(f"Request URL: {response.url}")           # ✅ Debug URL
            print(f"Response Status Code: {response.status_code}")  # ✅ Debug Status
            print(f"Response Text: {response.text[:500]}")  # ✅ Limit output to 500 chars

            # Ensure response is valid JSON
            if response.status_code == 200:
                total_records = response.json()
            else:
                raise ValueError(f"Error {response.status_code}: {response.text}")

        except Exception as e:
            print(f"Error fetching data: {e}")
            return pd.DataFrame()

        # Fetch paginated data
        while offset < total_records:
            url = f"{self.base_url}/{dataset}/data?limit={limit}&offset={offset}{filter_query}"
            try:
                response = requests.get(url, headers=self.headers)
                if response.status_code == 200:
                    data.extend(response.json())
                else:
                    print(f"Pagination Error {response.status_code}: {response.text}")
                offset += limit
            except Exception as e:
                print(f"Error fetching data: {e}")
                break

        return pd.DataFrame(data)