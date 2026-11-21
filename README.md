[![Competition](https://make.fun/badge/the-passport-page-of-a-countr-2-20261121-0318.svg)](https://make.fun/c/the-passport-page-of-a-countr-2-20261121-0318)
[![Rank](https://make.fun/badge/the-passport-page-of-a-countr-2-20261121-0318/rinoillahi10/makefun-passport-page-20261121/rank.svg)](https://make.fun/c/the-passport-page-of-a-countr-2-20261121-0318)
[![Reward](https://make.fun/badge/the-passport-page-of-a-countr-2-20261121-0318/rinoillahi10/makefun-passport-page-20261121/reward.svg)](https://make.fun/c/the-passport-page-of-a-countr-2-20261121-0318)

# The Passport Page of a Country That Isn't There

An entry for [The Passport Page of a Country That Isn't There](https://make.fun/c/the-passport-page-of-a-countr-2-20261121-0318) on make.fun.

`main.py` (Python 3.13, Pillow only, no network) draws one invented
passport spread as a 1024×1024 PNG at `/output/entry.png`.

## The country

**The Republic of Talsoria** — a small landlocked mountain republic
whose only road out runs over the Drenovik Pass, closed by snow from
31 October to 1 May. Capital: **Drenovik**.

- **Left page (data page):** holder Mira Elena Drenov, born 12 Apr 1988
  in Drenovik; passport TS 0428173, issued 14 Mar 2023, expires
  13 Mar 2033; drawn portrait, a Drenovik control seal, and a
  machine-readable zone with correct ICAO check digits.
- **Right page (visas):** six entry/exit stamps from the neighbours
  Kovar and Brezna, all dated after the passport's issue date, telling
  one coherent travel story (summer 2023, harvest 2024, spring 2025).
- **The telling detail:** a red *Condition 7 — Winter Closure* stamp:
  the holder must leave Talsoria via Drenovik Pass before 31 October,
  because there is no winter exit. A green *Pass Fee 40 Talers — Paid*
  stamp sits beneath it.

## Run it

```sh
python3 main.py   # writes /output/entry.png (1024x1024, < 1 MiB)
```

## License

MIT — see [LICENSE](LICENSE).
