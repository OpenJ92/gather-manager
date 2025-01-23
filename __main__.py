from asyncio import run
from io import BytesIO
from sc2reader import load_replay
from sc2reader.exceptions import MPQError

from gather_manager.gatherable.download_link import DownloadLink
from storage_bridge.asynchro.local import AsyncLocalStorage

async def main():
    start = 16719051
    start = 256258
    for specifier in range(start, start-5, -1):
        url_formatter = lambda id: f"https://sc2replaystats.com/download/{id}"
        url_formatter = lambda id: f"https://www.rts-sanctuary.com/StarCraft-2/act=Attach&type=post&id={id}" # 403
        url_formatter = lambda id: f"https://lotv.spawningtool.com/{id}/download/"
        url_formatter = lambda id: f"https://www.gamereplays.org/starcraft2/replays.php?game=33&show=download&&id={id}"
        gatherable = DownloadLink(url_formatter, specifier)
        print(url_formatter(specifier))

        payload = await gatherable.gather()
        try:
            replay = load_replay(BytesIO(payload), load_level=1)
        except MPQError as e:
            print(e)
            continue

        external = AsyncLocalStorage("/app/external")
        release_string = replay.release_string.replace('.', '_')
        save_path = f"/app/external/{replay.filehash}.{release_string}.{replay.map_hash}.SC2Replay"
        await external.async_save(payload, save_path)

        replay_external = load_replay(save_path, load_level=4)

if __name__ == "__main__":
    run(main())
