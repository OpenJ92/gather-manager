from asyncio import run
from sc2reader import load_replay

from gather_manager.gatherable.download_link import DownloadLink
from storage_bridge.asynchro.local import AsyncLocalStorage

async def main():
    specifier = 16719051
    url_formatter = lambda id: f"https://sc2replaystats.com/download/{id}"
    gatherable = DownloadLink(url_formatter, specifier)

    payload = await gatherable.gather()
    print(f"Payload type: {type(payload)}, length: {len(payload)}")

    local = AsyncLocalStorage("/app/internal")

    await local.async_save(payload, f"/app/internal/{specifier}.SC2Replay")
    replay = load_replay(f"/app/internal/{specifier}.SC2Replay", load_level=1)
    await local.async_delete(f"/app/internal/{specifier}.SC2Replay")

    external = AsyncLocalStorage("/app/external")
    release_string = replay.release_string.replace('.', '_')
    save_path = f"/app/external/{replay.filehash}.{release_string}.{replay.map_hash}.SC2Replay"
    await external.async_save(payload, save_path)

    replay_external = load_replay(save_path, load_level=4)

    breakpoint()

if __name__ == "__main__":
    run(main())
