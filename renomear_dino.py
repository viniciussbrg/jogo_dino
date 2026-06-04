#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Renomeia os .circ do projeto Dino para portugues e atualiza
as referencias internas (<lib desc="file#...">).
Rode este script DENTRO da pasta onde estao os .circ originais.
Cria os arquivos novos numa subpasta 'pt/'. Nao apaga nada.
"""
import os, sys

# Forca a saida do console em UTF-8 quando possivel (Windows cp1252 nao
# consegue imprimir caracteres como 's-acento'); se falhar, seguimos mesmo assim.
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

def msg(s):
    """imprime sem nunca quebrar por causa de encoding do console."""
    try:
        print(s)
    except Exception:
        print(s.encode("ascii", "replace").decode("ascii"))

MAPA = {
    "proba2.circ":                    "principal.circ",
    "skroceniev2 led.circ":           "tela_led.circ",
    "przegrana.circ":                 "game_over.circ",
    "wynik wyświetlanie duży.circ":   "pontuacao_exibicao.circ",
    "wynik wyświetlanie mały.circ":   "pontuacao_digito.circ",
    "mały_lub_duży.circ":             "obstaculo_tamanho.circ",
    "clock zmiana.circ":              "clock_seletor.circ",
    "dinozaur wyswietlanie.circ":     "dino_sprite.circ",
    "kaktus wyswietlanie.circ":       "cacto_sprite.circ",
    "ptaki.circ":                     "passaros.circ",
    "probaled2.circ":                 "colisao_cenario.circ",
}

SAIDA = "pt"
os.makedirs(SAIDA, exist_ok=True)

faltando = [a for a in MAPA if not os.path.exists(a)]
if faltando:
    msg("AVISO: nao encontrei estes arquivos na pasta atual:")
    for f in faltando:
        msg("   - " + f)
    msg("")

feitos = 0
for antigo, novo in MAPA.items():
    if not os.path.exists(antigo):
        continue
    with open(antigo, "r", encoding="utf-8") as fh:
        txt = fh.read()
    for a2, n2 in MAPA.items():
        txt = txt.replace("file#" + a2, "file#" + n2)
    with open(os.path.join(SAIDA, novo), "w", encoding="utf-8") as fh:
        fh.write(txt)
    feitos += 1
    msg("OK: " + antigo + "  ->  " + SAIDA + "/" + novo)

msg("")
msg("Concluido: " + str(feitos) + " de " + str(len(MAPA)) + " arquivos.")
msg("Abra '" + SAIDA + "/principal.circ' no Logisim.")
msg("Mantenha todos os .circ da pasta '" + SAIDA + "' juntos.")
