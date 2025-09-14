import asyncio
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))

from app.db.session import SessionLocal
from app.services.player_data_service import sync_nflverse_players, sync_fantasy_calc_values

async def main():
    print("Seeding player data...")
    db = SessionLocal()
    
    try:
        await sync_nflverse_players(db)
        await sync_fantasy_calc_values(db)
    except Exception as e:
        print(f"An error occurred during data seeding: {e}")
        await db.rollback()
    finally:
        await db.close()

    print("Player data seeding complete.")

if __name__ == "__main__":
    asyncio.run(main())
