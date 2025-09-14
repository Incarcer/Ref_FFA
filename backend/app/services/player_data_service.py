import asyncio
import httpx
import pandas as pd
import io
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from ..models.player import Player, PlayerSourceMapping, PlayerValue, Position, ScoringFormat

POSITION_MAP = {
    "QB": Position.QB,
    "RB": Position.RB,
    "WR": Position.WR,
    "TE": Position.TE,
    "K": Position.K,
    "DEF": Position.DEF,
}

NFLVERSE_ROSTERS_URL = "https://github.com/nflverse/nflverse-data/blob/master/rosters/rosters_2023.csv?raw=true"
FANTASYCALC_VALUES_URL = "https://fantasycalc.com/api/v1/values/superflex"

async def sync_nflverse_players(db: AsyncSession):
    print("Starting nflverse player sync...")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(NFLVERSE_ROSTERS_URL, timeout=30.0)
            response.raise_for_status()
    except httpx.RequestError as e:
        print(f"Error fetching nflverse data: {e}")
        return

    roster_data = pd.read_csv(io.StringIO(response.text))
    roster_data = roster_data.where(pd.notnull(roster_data), None)

    relevant_cols = ['player_id', 'player_name', 'position', 'team', 'fantasypros_id']
    players_to_process = roster_data[relevant_cols].to_dict('records')
    
    new_players = 0
    new_mappings = 0

    for player_data in players_to_process:
        if not all(player_data.get(k) for k in ['player_id', 'player_name', 'position']):
            continue

        fantasypros_id_raw = player_data.get('fantasypros_id')
        fantasypros_id = str(int(fantasypros_id_raw)) if fantasypros_id_raw else None
        
        nflverse_id = player_data['player_id']
        
        player = None
        if fantasypros_id:
            stmt = select(PlayerSourceMapping).where(
                PlayerSourceMapping.source == 'fantasypros',
                PlayerSourceMapping.external_id == fantasypros_id
            )
            result = await db.execute(stmt)
            mapping = result.scalars().first()
            if mapping:
                player = await db.get(Player, mapping.player_id)

        if not player:
            pos = player_data.get('position')
            if pos not in POSITION_MAP:
                continue

            player = Player(
                name=player_data['player_name'],
                position=POSITION_MAP[pos],
                nfl_team_abbr=player_data.get('team')
            )
            db.add(player)
            await db.flush()
            new_players += 1
        
        if fantasypros_id:
            stmt_fp = select(PlayerSourceMapping).where(PlayerSourceMapping.player_id == player.id, PlayerSourceMapping.source == 'fantasypros')
            if not (await db.execute(stmt_fp)).scalars().first():
                db.add(PlayerSourceMapping(player_id=player.id, source='fantasypros', external_id=fantasypros_id))
                new_mappings += 1

        stmt_nv = select(PlayerSourceMapping).where(PlayerSourceMapping.player_id == player.id, PlayerSourceMapping.source == 'nflverse')
        if not (await db.execute(stmt_nv)).scalars().first():
            db.add(PlayerSourceMapping(player_id=player.id, source='nflverse', external_id=nflverse_id))
            new_mappings += 1

    await db.commit()
    print(f"nflverse player sync finished. Created {new_players} new players and {new_mappings} new mappings.")


async def sync_fantasy_calc_values(db: AsyncSession):
    print("Starting fantasycalc value sync...")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(FANTASYCALC_VALUES_URL, timeout=30.0)
            response.raise_for_status()
    except httpx.RequestError as e:
        print(f"Error fetching fantasycalc data: {e}")
        return

    values_data = response.json()
    new_values = 0

    for item in values_data:
        fantasypros_id = item.get('player_id')
        value = item.get('value')

        if not fantasypros_id or not value:
            continue
            
        fantasypros_id = str(fantasypros_id)

        stmt = select(PlayerSourceMapping).where(
            PlayerSourceMapping.source == 'fantasypros',
            PlayerSourceMapping.external_id == fantasypros_id
        )
        result = await db.execute(stmt)
        mapping = result.scalars().first()

        if mapping:
            new_value = PlayerValue(
                player_id=mapping.player_id,
                source='fantasycalc',
                value=value,
                format=ScoringFormat.SUPERFLEX
            )
            db.add(new_value)
            new_values += 1

    await db.commit()
    print(f"fantasycalc value sync finished. Added {new_values} new player values.")
