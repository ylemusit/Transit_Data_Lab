# Kbus source identity verification

## Status

**CONFIRMED**

## Evidence observed in source

- Original ZIP: `20250530_060158_Bus_Barakaldo.zip`. The filename contains `Barakaldo`.
- `agency.txt`: `agency_id=kbus`, `agency_name=Kbus`.
- `agency_url`: `https://www.kbus.eus/`.
- `routes.txt`: 4 routes; route URLs point to the Kbus website: `https://www.kbus.eus/lineas-y-horarios`.
- `stops.txt`: 88 stops. The following observed stop names are consistent with the Barakaldo network context: Altos Hornos 1, Altos Hornos 2, Altos Hornos 26, Altos Hornos 27, Polideportivo Lasesarre Kiroldegia, Polideportivo Lasesarre Kiroldegia (Sentido horario), Retuerto (Avenida Euskadi Etorbidea), Retuerto (Avenida Euskadi Etorbidea, sentido horario).
- The source ZIP and the existing operator folder are paired as `020_kbus`; no file was moved or modified.

## Scope note

This confirms the physical association of the source with Kbus/Barakaldo. It is not a regulatory or semantic validation of the feed.
