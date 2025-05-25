import json
from typing import List, Dict, Any, Optional, Union

def get_shows(file_path: str = "shows.json", show_id: Optional[int] = None) -> Union[List[Dict], Dict]:
   with open(file_path,"r", encoding="utf-8") as fh:
        shows = json.load(fh)

        if show_id is not None and 0 <= show_id < len(shows):
            return shows[show_id]
   
        return shows