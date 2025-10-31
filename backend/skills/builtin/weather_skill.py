"""
Weather Skill (v0.4)
Get weather information using wttr.in (no API key needed)
"""
import aiohttp
from core.skill_base import Skill, SkillMetadata
from typing import Dict, Any


class WeatherSkill(Skill):
    """Get weather information"""
    
    def get_metadata(self) -> SkillMetadata:
        return SkillMetadata(
            name="weather",
            version="1.0.0",
            author="NuxAI Team",
            description="Get current weather and forecast",
            triggers=["weather", "temperature", "forecast", "what's the weather"]
        )
    
    async def execute(self, command: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Get weather information"""
        # Extract location from command or use default
        location = self._extract_location(command) or "auto"
        
        try:
            weather_info = await self._fetch_weather(location)
            
            response = f"The weather in {weather_info['location']} is {weather_info['condition']} "
            response += f"with a temperature of {weather_info['temperature']}"
            
            return {
                "success": True,
                "result": weather_info,
                "speak": response
            }
        except Exception as e:
            self.logger.error(f"Weather fetch error: {e}")
            return {
                "success": False,
                "error": "Could not fetch weather information",
                "speak": "Sorry, I couldn't get the weather right now"
            }
    
    def _extract_location(self, command: str) -> str:
        """Extract location from command"""
        # Simple extraction - look for "in [location]"
        words = command.lower().split()
        if "in" in words:
            idx = words.index("in")
            if idx + 1 < len(words):
                return " ".join(words[idx+1:])
        return None
    
    async def _fetch_weather(self, location: str) -> Dict[str, str]:
        """Fetch weather from wttr.in"""
        url = f"https://wttr.in/{location}?format=j1"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    current = data['current_condition'][0]
                    
                    return {
                        "location": data['nearest_area'][0]['areaName'][0]['value'],
                        "temperature": f"{current['temp_C']}°C ({current['temp_F']}°F)",
                        "condition": current['weatherDesc'][0]['value'],
                        "humidity": f"{current['humidity']}%",
                        "wind": f"{current['windspeedKmph']} km/h"
                    }
                else:
                    raise Exception(f"Weather API returned {response.status}")

