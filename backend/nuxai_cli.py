#!/usr/bin/env python3
"""
NuxAI CLI (v0.4+)
Command-line interface for managing NuxAI
"""
import argparse
import asyncio
import sys
from pathlib import Path
from core.skill_manager import SkillManager
from utils.logger import setup_logger

logger = setup_logger(__name__)


async def list_skills():
    """List all available skills"""
    manager = SkillManager()
    await manager.load_all_skills()
    
    skills = manager.list_skills()
    
    if not skills:
        print("No skills loaded")
        return
    
    print("\n📦 NuxAI Skills:\n")
    for skill in skills:
        status = "✅" if skill["enabled"] else "❌"
        print(f"{status} {skill['name']} v{skill['version']}")
        print(f"   {skill['description']}")
        print(f"   Triggers: {', '.join(skill['triggers'])}")
        print(f"   Author: {skill['author']}\n")


async def enable_skill(name: str):
    """Enable a skill"""
    manager = SkillManager()
    await manager.load_all_skills()
    manager.enable_skill(name)
    print(f"✅ Enabled skill: {name}")


async def disable_skill(name: str):
    """Disable a skill"""
    manager = SkillManager()
    await manager.load_all_skills()
    manager.disable_skill(name)
    print(f"❌ Disabled skill: {name}")


async def test_skill(name: str, command: str):
    """Test a skill with a command"""
    manager = SkillManager()
    await manager.load_all_skills()
    
    skill = manager.get_skill(name)
    if not skill:
        print(f"❌ Skill not found: {name}")
        return
    
    print(f"🧪 Testing skill '{name}' with command: '{command}'")
    result = await skill.execute(command, {})
    
    print("\nResult:")
    print(f"  Success: {result.get('success')}")
    if result.get('result'):
        print(f"  Result: {result['result']}")
    if result.get('speak'):
        print(f"  Speech: {result['speak']}")
    if result.get('error'):
        print(f"  Error: {result['error']}")


def create_skill(name: str):
    """Create a new skill template"""
    template = f'''"""
{name.title()} Skill
Custom skill for NuxAI
"""
from core.skill_base import Skill, SkillMetadata
from typing import Dict, Any


class {name.title()}Skill(Skill):
    """Description of your skill"""
    
    def get_metadata(self) -> SkillMetadata:
        return SkillMetadata(
            name="{name}",
            version="1.0.0",
            author="Your Name",
            description="What does this skill do?",
            triggers=["trigger word 1", "trigger word 2"]
        )
    
    async def execute(self, command: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the skill"""
        # Your skill logic here
        
        return {{
            "success": True,
            "result": "Skill executed",
            "speak": "Voice response here"
        }}
'''
    
    filename = f"skills/user/{name}_skill.py"
    filepath = Path(filename)
    
    if filepath.exists():
        print(f"❌ Skill already exists: {filename}")
        return
    
    filepath.write_text(template)
    print(f"✅ Created skill template: {filename}")
    print("\nEdit the file to implement your skill, then run:")
    print(f"  python nuxai_cli.py --test {name} 'your test command'")


def main():
    parser = argparse.ArgumentParser(
        description="NuxAI CLI - Manage your AI assistant",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  nuxai_cli.py --list-skills           List all skills
  nuxai_cli.py --enable weather        Enable weather skill
  nuxai_cli.py --disable weather       Disable weather skill
  nuxai_cli.py --test weather "weather in London"
  nuxai_cli.py --create myskill        Create new skill template
        """
    )
    
    parser.add_argument("--list-skills", action="store_true",
                        help="List all available skills")
    parser.add_argument("--enable", metavar="SKILL",
                        help="Enable a skill")
    parser.add_argument("--disable", metavar="SKILL",
                        help="Disable a skill")
    parser.add_argument("--test", nargs=2, metavar=("SKILL", "COMMAND"),
                        help="Test a skill with a command")
    parser.add_argument("--create", metavar="NAME",
                        help="Create a new skill template")
    
    args = parser.parse_args()
    
    if args.list_skills:
        asyncio.run(list_skills())
    elif args.enable:
        asyncio.run(enable_skill(args.enable))
    elif args.disable:
        asyncio.run(disable_skill(args.disable))
    elif args.test:
        asyncio.run(test_skill(args.test[0], args.test[1]))
    elif args.create:
        create_skill(args.create)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

