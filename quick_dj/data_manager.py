import json
from typing import Dict, List, Union


class DataManager:
    def __init__(self, file: str = 'data.json') -> None:
        self.file: str = file
        self.data: Dict[str, Dict[str, Dict[str, Union[Dict[str, Union[str, List[Dict[str, str]]]], Dict[str, Dict[str, Union[str, List[Dict[str, str]]]]]]]]] = self._load_data()

    def _load_data(self) -> Dict[str, Dict[str, Dict[str, Union[Dict[str, Union[str, List[Dict[str, str]]]], Dict[str, Dict[str, Union[str, List[Dict[str, str]]]]]]]]]:
        with open(self.file, 'r') as f:
            return json.load(f)

    def _save_data(self) -> None:
        with open(self.file, 'w') as f:
            json.dump(self.data, f)

    def create_app(self, app_name: str) -> None:
        self.data["apps"][app_name] = {"models": {}}
        self._save_data()

    def create_model(self, app_name: str, model_name: str) -> None:
        self.data["apps"][app_name]["models"][model_name] = {"fields": {}}
        self._save_data()

    def create_field(self, app_name: str, model_name: str, field_name: str, field_type: str) -> None:
        self.data["apps"][app_name]["models"][model_name]["fields"][field_name] = {
            "type": field_type,
            "options": []
        }
        self._save_data()

    def create_option(self, app_name: str, model_name: str, field_name: str, option_name: str, option_value: str) -> None:
        self.data["apps"][app_name]["models"][model_name]["fields"][field_name]["options"].append({
            "name": option_name,
            "value": option_value
        })
        self._save_data()

    def delete_app(self, app_name: str) -> None:
        del self.data["apps"][app_name]
        self._save_data()

    def delete_model(self, app_name: str, model_name: str) -> None:
        del self.data["apps"][app_name]["models"][model_name]
        self._save_data()

    def delete_field(self, app_name: str, model_name: str, field_name: str) -> None:
        del self.data["apps"][app_name]["models"][model_name]["fields"][field_name]
        self._save_data()

    def delete_option(self, app_name: str, model_name: str, field_name: str, option_name: str) -> None:
        options: List[Dict[str, str]] = self.data["apps"][app_name]["models"][model_name]["fields"][field_name]["options"]
        for i, option in enumerate(options):
            if option["name"] == option_name:
                del options[i]
                break
        self._save_data()