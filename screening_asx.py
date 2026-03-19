#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════╗
║      ASX PROFESSIONAL SCREENING SYSTEM  —  v9.0.0                   ║
║      Strategi: Professional Commodities & Energy Desk 2026              ║
║                                                                      ║
║  Coverage : Coal · Iron Ore · Lithium · Rare Earth · Copper         ║
║             Energy · Oil & Gas · Uranium · Gold                      ║
║  Filter   : Harga < AUD $10  |  Multi-Factor Scoring                ║
║  Signals  : RSI14 · RSI7 · BB · MA · EMA · MACD · ATR · Volume     ║
║             Stochastic · OBV · Williams%R · CCI · Candle · Pivot    ║
║  Run      : python screening_asx.py                                  ║
╚══════════════════════════════════════════════════════════════════════╝

  ⚠  DISCLAIMER: Alat ini hanya untuk tujuan edukasi dan riset.
     Bukan merupakan saran investasi. Selalu lakukan riset mandiri.
"""

import os, time, sys, statistics
import requests
from datetime import datetime

# ══════════════════════════════════════════════════════════════════════
#  WATCHLIST — ASX COMMODITIES & ENERGY 2026
#  Conviction Rating:
#  ★★★★★ Highest  |  ★★★★ High  |  ★★★ Moderate  |  ★★ Watch  |  ★ Speculative
# ══════════════════════════════════════════════════════════════════════
watchlist = [

    # ────────────────────────────────────────────────────────────────
    #  COAL — Coking & Thermal
    #  Thesis: India/SE Asia steel demand, supply tightness 2026
    # ────────────────────────────────────────────────────────────────
    {"s":"YAL.AX","n":"YAL","sector":"COAL",
     "note":"Yancoal · thermal coal · dividend yield tinggi","stars":"★★★★",
     "catalyst":"Div yield ~10%, kontrak Asia jangka panjang"},
    {"s":"WHC.AX","n":"WHC","sector":"COAL",
     "note":"Whitehaven · premium metallurgical coal","stars":"★★★★★",
     "catalyst":"Ekspansi Winchester South, demand India naik"},
    {"s":"CRN.AX","n":"CRN","sector":"COAL",
     "note":"Coronado · coking coal · US+AU ops","stars":"★★★★",
     "catalyst":"Harga coking coal rebound, operasi Curragh efisien"},
    {"s":"BCB.AX","n":"BCB","sector":"COAL",
     "note":"Bowen Coking · PCI coal · ekspansi 2026","stars":"★★★",
     "catalyst":"Ramp-up Broadmeadow East, cash flow positif"},
    {"s":"TIG.AX","n":"TIG","sector":"COAL",
     "note":"Tigers Realm · Kamchikskiy mine","stars":"★★",
     "catalyst":"Produksi stabil, valuasi murah"},
    {"s":"AKM.AX","n":"AKM","sector":"COAL",
     "note":"Aspire Mining · Mongolia coking coal","stars":"★★",
     "catalyst":"Pembangunan rel kereta Mongolia"},

    # ────────────────────────────────────────────────────────────────
    #  MINING / IRON ORE
    #  Thesis: China stimulus, steel restocking H2 2026
    # ────────────────────────────────────────────────────────────────
    {"s":"FMG.AX","n":"FMG","sector":"MINING",
     "note":"Fortescue · iron ore giant · green energy pivot","stars":"★★★★★",
     "catalyst":"FFI green hydrogen, capex turun, div tinggi"},
    {"s":"MGX.AX","n":"MGX","sector":"MINING",
     "note":"Mount Gibson Iron · high-grade ore","stars":"★★★",
     "catalyst":"Koolan Island produksi penuh, cash pile besar"},
    {"s":"GRR.AX","n":"GRR","sector":"MINING",
     "note":"Grange Resources · iron ore pellets premium","stars":"★★★",
     "catalyst":"Pellet premium vs fines, kontrak Jepang"},
    {"s":"CIA.AX","n":"CIA","sector":"MINING",
     "note":"Champion Iron · Quebec DR-grade ore","stars":"★★★★",
     "catalyst":"Bloom Lake fasa 2 penuh, ore >66% Fe premium"},
    {"s":"SRK.AX","n":"SRK","sector":"MINING",
     "note":"Strike Resources · Paulsens East","stars":"★★",
     "catalyst":"Drill results 2026, eksplorasi aktif"},
    {"s":"ACS.AX","n":"ACS","sector":"MINING",
     "note":"Accent Resources · early stage","stars":"★",
     "catalyst":"Spekulatif, target area WA"},
    {"s":"GCM.AX","n":"GCM","sector":"MINING",
     "note":"GCM Corp · teknologi thermal VHD","stars":"★★★★",
     "catalyst":"Komersialisasi VHD H1 2026, listing AS, MoU Korea"},
    {"s":"NIC.AX","n":"NIC","sector":"MINING",
     "note":"Nickel Industries · Indonesia HPAL","stars":"★★★★",
     "catalyst":"EV supply chain, HPAL ekspansi, partner Tsingshan"},
    {"s":"MIN.AX","n":"MIN","sector":"MINING",
     "note":"Mineral Resources · lithium + iron ore","stars":"★★★★",
     "catalyst":"Debt reduction plan, Onslow iron ore ramp-up"},

    # ────────────────────────────────────────────────────────────────
    #  LITHIUM
    #  Thesis: EV recovery 2026, China restocking, harga floor tercapai
    # ────────────────────────────────────────────────────────────────
    {"s":"PLS.AX","n":"PLS","sector":"LITHIUM",
     "note":"Pilbara Minerals · lithium spodumene terbesar","stars":"★★★★★",
     "catalyst":"P680 ekspansi, harga litium rebound, balance sheet kuat"},
    {"s":"LTR.AX","n":"LTR","sector":"LITHIUM",
     "note":"Liontown · Kathleen Valley mine baru","stars":"★★★★",
     "catalyst":"Produksi perdana 2025-26, offtake Ford & LG"},
    {"s":"IGO.AX","n":"IGO","sector":"LITHIUM",
     "note":"IGO Limited · lithium-nickel hybrid","stars":"★★★★",
     "catalyst":"Greenbushes royalty, cash flow stabil"},
    {"s":"SYA.AX","n":"SYA","sector":"LITHIUM",
     "note":"Sayona Mining · Quebec ops","stars":"★★★",
     "catalyst":"North American Lithium restart, Piedmont offtake"},
    {"s":"GL1.AX","n":"GL1","sector":"LITHIUM",
     "note":"Global Lithium · Marble Bar WA","stars":"★★★",
     "catalyst":"Resource upgrade, DFS 2026"},
    {"s":"LKE.AX","n":"LKE","sector":"LITHIUM",
     "note":"Lake Resources · Kachi brine Argentina","stars":"★★★",
     "catalyst":"Direct lithium extraction tech, offtake Hanwa"},
    {"s":"CXO.AX","n":"CXO","sector":"LITHIUM",
     "note":"Core Lithium · Finniss mine NT","stars":"★★★",
     "catalyst":"Restart decision bergantung harga litium"},
    {"s":"ARL.AX","n":"ARL","sector":"LITHIUM",
     "note":"Ardea Resources · nickel-cobalt WA","stars":"★★",
     "catalyst":"Kalgoorlie Nickel Project PFS"},
    {"s":"INF.AX","n":"INF","sector":"LITHIUM",
     "note":"Infinity Lithium · Spain EU battery","stars":"★★★",
     "catalyst":"EU Critical Raw Materials Act, San Jose project"},
    {"s":"VUL.AX","n":"VUL","sector":"LITHIUM",
     "note":"Vulcan Energy · zero carbon lithium Germany","stars":"★★★★",
     "catalyst":"EU gigafactory offtake, geothermal energy bonus"},

    # ────────────────────────────────────────────────────────────────
    #  RARE EARTH
    #  Thesis: China export restrictions, EV magnet demand, defence
    # ────────────────────────────────────────────────────────────────
    {"s":"LYC.AX","n":"LYC","sector":"RARE EARTH",
     "note":"Lynas · rare earth terbesar non-China","stars":"★★★★★",
     "catalyst":"China export ban RE, US Dept Defence kontrak, Kalgoorlie plant"},
    {"s":"ARU.AX","n":"ARU","sector":"RARE EARTH",
     "note":"Arafura RE · Nolans NdPr project NT","stars":"★★★★",
     "catalyst":"Government funding, Siemens Gamesa offtake, DFS selesai"},
    {"s":"HAS.AX","n":"HAS","sector":"RARE EARTH",
     "note":"Hastings Technology · Yangibana WA","stars":"★★★",
     "catalyst":"Produksi NdPr 2026, harga RE naik"},
    {"s":"NTU.AX","n":"NTU","sector":"RARE EARTH",
     "note":"Northern Minerals · Browns Range Dy","stars":"★★★",
     "catalyst":"Dysprosium strategis, pilot plant results"},
    {"s":"OD6.AX","n":"OD6","sector":"RARE EARTH",
     "note":"OD6 Metals · scandium WA","stars":"★★★",
     "catalyst":"Scandium untuk aerospace & EV"},
    {"s":"EMN.AX","n":"EMN","sector":"RARE EARTH",
     "note":"Euro Manganese · Czech Republic","stars":"★★★",
     "catalyst":"EU battery-grade manganese, gigafactory supply"},
    {"s":"TMR.AX","n":"TMR","sector":"RARE EARTH",
     "note":"Tempus Resources · Colombia gold-RE","stars":"★★",
     "catalyst":"Eksplorasi aktif, dual commodity"},

    # ────────────────────────────────────────────────────────────────
    #  COPPER
    #  Thesis: Grid electrification, EV, AI data centre 2026-2030
    # ────────────────────────────────────────────────────────────────
    {"s":"SFR.AX","n":"SFR","sector":"COPPER",
     "note":"Sandfire Resources · MATSA Spain + Botswana","stars":"★★★★★",
     "catalyst":"Motheo ramp-up, harga Cu >$10k/t, produksi naik 30%"},
    {"s":"AIS.AX","n":"AIS","sector":"COPPER",
     "note":"Aeris Resources · Tritton + Cracow","stars":"★★★★",
     "catalyst":"Cobar basin ekspansi, rerating potensi"},
    {"s":"29M.AX","n":"29M","sector":"COPPER",
     "note":"29Metals · copper-zinc Capricorn","stars":"★★★",
     "catalyst":"Recovery post-flood, insurance claim resolved"},
    {"s":"C6C.AX","n":"C6C","sector":"COPPER",
     "note":"Copper 6C · early exploration","stars":"★★",
     "catalyst":"Drill program 2026, high-grade intercepts"},
    {"s":"MOD.AX","n":"MOD","sector":"COPPER",
     "note":"MOD Resources · T3 Botswana","stars":"★★★",
     "catalyst":"Khoemacau Phase 2, copper demand EV"},
    {"s":"WC8.AX","n":"WC8","sector":"COPPER",
     "note":"West Cobar Metals · Gilgunnia NSW","stars":"★★",
     "catalyst":"Drill results 2026, proximity infrastructure"},

    # ════════════════════════════════════════════════════════════════
    #  ENERGY — OIL & GAS 2026
    #  ── Pro Trader Conviction Picks ──
    #  Thesis: Geopolitik → minyak bertahan $75-90
    #          LNG Asia demand tinggi (Japan, Korea, India)
    #          Australia gas shortage domestik → harga domestik naik
    #          Dividen & buyback menarik vs sektor lain
    # ════════════════════════════════════════════════════════════════

    # TIER 1 — HIGH CONVICTION 2026
    {"s":"WDS.AX","n":"WDS","sector":"ENERGY ★★★★★",
     "note":"Woodside · LNG raksasa · Scarborough+Pluto T2","stars":"★★★★★",
     "catalyst":"Scarborough onstream 2026, LNG spot Asia premium, div yield ~7-8%"},
    {"s":"STO.AX","n":"STO","sector":"ENERGY ★★★★★",
     "note":"Santos · Barossa LNG + PNG + Dorado oil","stars":"★★★★★",
     "catalyst":"Barossa FID done, PNG LNG ekspansi, Dorado oil dev, M&A target"},
    {"s":"BPT.AX","n":"BPT","sector":"ENERGY ★★★★",
     "note":"Beach Energy · Cooper Basin + Otway gas","stars":"★★★★",
     "catalyst":"Waitsia gas onstream WA, domestic gas premium, div naik"},

    # TIER 2 — OVERWEIGHT 2026
    {"s":"KAR.AX","n":"KAR","sector":"ENERGY ★★★★",
     "note":"Karoon Energy · Bauna Brazil + Who Dat US","stars":"★★★★",
     "catalyst":"Bauna debottleneck, cash cow, buyback program, oil >$75"},
    {"s":"STX.AX","n":"STX","sector":"ENERGY ★★★★",
     "note":"Strike Energy · West Erregulla gas WA","stars":"★★★★",
     "catalyst":"Gas shortage WA domestik, FID West Erregulla 2026, harga gas naik"},
    {"s":"NHC.AX","n":"NHC","sector":"ENERGY ★★★★",
     "note":"New Hope Corp · coal + Acland stage 3","stars":"★★★★",
     "catalyst":"Acland Stage 3 approved, thermal coal demand Asia, div yield ~12%"},

    # TIER 3 — NEUTRAL/WATCH dengan UPSIDE
    {"s":"COE.AX","n":"COE","sector":"ENERGY ★★★",
     "note":"Cooper Energy · Orbost gas Vic","stars":"★★★",
     "catalyst":"Orbost plant optimasi, domestic gas contract SE Australia"},
    {"s":"HZN.AX","n":"HZN","sector":"ENERGY ★★★",
     "note":"Horizon Oil · PNG + Crab Island gas","stars":"★★★",
     "catalyst":"PNG gas monetisasi, low-cost producer"},
    {"s":"CVN.AX","n":"CVN","sector":"ENERGY ★★★",
     "note":"Carnarvon Energy · Dorado oil WA (Santos partner)","stars":"★★★",
     "catalyst":"Dorado development FID, leverage ke Santos ops"},
    {"s":"DGR.AX","n":"DGR","sector":"ENERGY ★★★",
     "note":"DGR Global · oil sands + gold exposure","stars":"★★★",
     "catalyst":"Commodity diversifikasi, NAV discount besar"},

    # TIER 4 — SPECULATIVE HIGH UPSIDE (Kecil tapi potensi 2-5x)
    {"s":"HAV.AX","n":"HAV","sector":"ENERGY ★★",
     "note":"Havilah Resources · Kalkaroo copper-gold-cobalt","stars":"★★",
     "catalyst":"Financing deal, copper-gold drill 2026"},
    {"s":"WGO.AX","n":"WGO","sector":"ENERGY ★★",
     "note":"Warrego Energy · West Erregulla (partner STX)","stars":"★★",
     "catalyst":"Leverage ke Strike Energy West Erregulla success"},
    {"s":"EME.AX","n":"EME","sector":"ENERGY ★★",
     "note":"Emperor Energy · Judith gas Vic offshore","stars":"★★",
     "catalyst":"Gas shortage Vic, Judith development path"},
    {"s":"RAU.AX","n":"RAU","sector":"ENERGY ★★",
     "note":"Regal Resources · NT oil exploration","stars":"★★",
     "catalyst":"Drill catalyst H1 2026, NT basin derisked"},

    # ────────────────────────────────────────────────────────────────
    #  URANIUM
    #  Thesis: Nuclear renaissance, AI data centre power demand
    # ────────────────────────────────────────────────────────────────
    {"s":"PDN.AX","n":"PDN","sector":"URANIUM",
     "note":"Paladin Energy · Langer Heinrich restart","stars":"★★★★★",
     "catalyst":"Langer Heinrich full prod, uranium >$85/lb, Fission merger"},
    {"s":"BOE.AX","n":"BOE","sector":"URANIUM",
     "note":"Boss Energy · Honeymoon SA ISR","stars":"★★★★★",
     "catalyst":"ISR production ramp, Alta Mesa US stake, spot uranium naik"},
    {"s":"DYL.AX","n":"DYL","sector":"URANIUM",
     "note":"Deep Yellow · Tumas Namibia","stars":"★★★★",
     "catalyst":"DFS complete, construction decision 2026, Namibia tier-1"},
    {"s":"BMN.AX","n":"BMN","sector":"URANIUM",
     "note":"Bannerman Energy · Etango Namibia","stars":"★★★★",
     "catalyst":"Etango-8 DFS optimised, uranium supercycle"},
    {"s":"LOT.AX","n":"LOT","sector":"URANIUM",
     "note":"Lotus Resources · Kayelekera Malawi","stars":"★★★",
     "catalyst":"Restart ready, low capex, uranium price trigger"},
    {"s":"PEN.AX","n":"PEN","sector":"URANIUM",
     "note":"Peninsula Energy · Lance ISR Wyoming USA","stars":"★★★",
     "catalyst":"US uranium preference post-Russia ban, Lance restart"},

    # ────────────────────────────────────────────────────────────────
    #  GOLD / SILVER
    #  Thesis: USD weakness, Fed cuts, geopolitik, gold >$3000/oz
    # ────────────────────────────────────────────────────────────────
    {"s":"RRL.AX","n":"RRL","sector":"GOLD",
     "note":"Regis Resources · McPhillamys + Duketon WA","stars":"★★★★★",
     "catalyst":"McPhillamys approval, gold >$3000, AISC turun"},
    {"s":"GOR.AX","n":"GOR","sector":"GOLD",
     "note":"Gold Road Resources · Gruyere 50% JV Gold Fields","stars":"★★★★★",
     "catalyst":"Gruyere ekspansi, takeover target Gold Fields"},
    {"s":"VAU.AX","n":"VAU","sector":"GOLD",
     "note":"Vault Minerals · Deflector + King of the Hills","stars":"★★★★",
     "catalyst":"KOTH ramp-up, Deflector silver credits, merger synergy"},
    {"s":"RED.AX","n":"RED","sector":"GOLD",
     "note":"Red 5 · King of the Hills WA","stars":"★★★★",
     "catalyst":"Production target 200koz/yr, leverage gold price"},
    {"s":"ALK.AX","n":"ALK","sector":"GOLD",
     "note":"Alkane Resources · Tomingley + McPhillamys","stars":"★★★",
     "catalyst":"Tomingley underground, gold price leverage"},
    {"s":"SBM.AX","n":"SBM","sector":"GOLD",
     "note":"St Barbara · Simberi PNG + Atlantic","stars":"★★★",
     "catalyst":"Simberi sulphide expansion, Atlantic Canada ops"},
]

# ══════════════════════════════════════════════════════════════════════
#  CONFIG
# ══════════════════════════════════════════════════════════════════════
SECTOR_ORDER = [
    "COAL","MINING","LITHIUM","RARE EARTH","COPPER",
    "ENERGY ★★★★★","ENERGY ★★★★","ENERGY ★★★","ENERGY ★★",
    "URANIUM","GOLD"
]
HARGA_MAKS = 10.0

# ANSI Colors
G="\033[92m"; R="\033[91m"; Y="\033[93m"; C="\033[96m"
W="\033[97m"; DM="\033[2m"; B="\033[1m";  RS="\033[0m"
M="\033[95m"; BL="\033[94m"; OR="\033[38;5;208m"

def clr(): os.system("cls" if os.name=="nt" else "clear")

def fp(p):
    if p is None or p==0: return "-.--"
    if p < 0.001: return f"{p:.5f}"
    if p < 0.01:  return f"{p:.4f}"
    if p < 1:     return f"{p:.3f}"
    return f"{p:.2f}"

def fvol(v):
    if v is None: return "   -  "
    if v>=1e9: return f"{v/1e9:.1f}B"
    if v>=1e6: return f"{v/1e6:.1f}M"
    if v>=1e3: return f"{v/1e3:.0f}K"
    return str(v)

def cpct(val):
    if val is None: return "   -   "
    col = G if val >= 1 else (R if val < 0 else Y)
    return f"{col}{val:>+6.2f}%{RS}"

def star_color(stars):
    n = stars.count("★")
    if n >= 5: return f"{G}{B}{stars}{RS}"
    if n >= 4: return f"{G}{stars}{RS}"
    if n >= 3: return f"{Y}{stars}{RS}"
    return f"{DM}{stars}{RS}"

# ══════════════════════════════════════════════════════════════════════
#  FETCH — Yahoo Finance
# ══════════════════════════════════════════════════════════════════════
def fetch(symbol):
    try:
        url = (f"https://query1.finance.yahoo.com/v8/finance/chart/"
               f"{symbol}?interval=5m&range=5d")
        r = requests.get(url, headers={"User-Agent":"Mozilla/5.0"}, timeout=15)
        r.raise_for_status()
        res  = r.json()["chart"]["result"][0]
        meta = res["meta"]
        price = meta.get("regularMarketPrice") or meta.get("previousClose", 0)
        prev  = meta.get("chartPreviousClose")  or meta.get("previousClose", price)
        high  = meta.get("regularMarketDayHigh")
        low   = meta.get("regularMarketDayLow")
        vol   = meta.get("regularMarketVolume")
        C_=[]; H_=[]; L_=[]
        try:
            q  = res.get("indicators",{}).get("quote",[{}])[0]
            C_ = [x for x in q.get("close",[]) if x]
            H_ = [x for x in q.get("high",[])  if x]
            L_ = [x for x in q.get("low",[])   if x]
        except: pass
        ma5  = statistics.mean(C_[-5:])  if len(C_)>=5  else None
        ma20 = statistics.mean(C_[-20:]) if len(C_)>=20 else None
        ma50 = statistics.mean(C_[-50:]) if len(C_)>=50 else None

        # EMA helper
        def ema(data, period):
            if len(data) < period: return None
            k = 2/(period+1)
            e = statistics.mean(data[:period])
            for x in data[period:]: e = x*k + e*(1-k)
            return round(e, 5)

        ema9  = ema(C_, 9)
        ema21 = ema(C_, 21)
        ema50 = ema(C_, 50)

        # RSI-14
        rsi = None
        if len(C_) >= 15:
            d = [C_[i]-C_[i-1] for i in range(1,len(C_))]
            g = sum(x for x in d[-14:] if x>0)/14
            l = sum(-x for x in d[-14:] if x<0)/14
            rsi = round(100-(100/(1+g/l)), 1) if l else 100.0

        # RSI-7 (short term)
        rsi7 = None
        if len(C_) >= 8:
            d7 = [C_[i]-C_[i-1] for i in range(1,len(C_))]
            g7 = sum(x for x in d7[-7:] if x>0)/7
            l7 = sum(-x for x in d7[-7:] if x<0)/7
            rsi7 = round(100-(100/(1+g7/l7)), 1) if l7 else 100.0

        # Bollinger Bands
        bbu=bbm=bbl=None
        bb_width=None; bb_pct=None
        if len(C_) >= 20:
            rc=C_[-20:]; m=statistics.mean(rc); s=statistics.stdev(rc)
            bbu=round(m+2*s,5); bbm=round(m,5); bbl=round(m-2*s,5)
            bb_width = round((bbu-bbl)/bbm*100, 2) if bbm else None
            if bbu and bbl and bbu != bbl:
                bb_pct = round((price-bbl)/(bbu-bbl)*100, 1)

        # ATR-14
        atr = None
        if len(C_) >= 14 and len(H_) >= 14 and len(L_) >= 14:
            trs=[]
            for i in range(1, min(len(C_),len(H_),len(L_))):
                trs.append(max(H_[i]-L_[i],
                               abs(H_[i]-C_[i-1]),
                               abs(L_[i]-C_[i-1])))
            if len(trs)>=14: atr=round(statistics.mean(trs[-14:]),5)

        # MACD (12,26,9)
        macd_line=macd_sig=macd_hist=None
        ema12 = ema(C_, 12); ema26 = ema(C_, 26)
        if ema12 and ema26:
            macd_line = round(ema12 - ema26, 5)
            # Signal line: EMA9 of MACD — approximate with last values
            if len(C_) >= 35:
                macd_vals=[]
                for i in range(9, len(C_)+1):
                    sl_e12 = ema(C_[:i], 12)
                    sl_e26 = ema(C_[:i], 26)
                    if sl_e12 and sl_e26:
                        macd_vals.append(sl_e12 - sl_e26)
                if len(macd_vals) >= 9:
                    macd_sig  = round(ema(macd_vals, 9) or 0, 5)
                    macd_hist = round(macd_line - macd_sig, 5)

        # Stochastic %K %D (14,3)
        stoch_k=stoch_d=None
        if len(C_)>=14 and len(H_)>=14 and len(L_)>=14:
            ks=[]
            for i in range(13, min(len(C_),len(H_),len(L_))):
                lo14 = min(L_[i-13:i+1]); hi14 = max(H_[i-13:i+1])
                if hi14 != lo14:
                    ks.append((C_[i]-lo14)/(hi14-lo14)*100)
            if ks:
                stoch_k = round(ks[-1], 1)
                stoch_d = round(statistics.mean(ks[-3:]), 1) if len(ks)>=3 else stoch_k

        # OBV (On Balance Volume)
        obv=None; obv_trend=None
        try:
            q2  = res.get("indicators",{}).get("quote",[{}])[0]
            vl2 = q2.get("volume",[])
            if len(C_)>=10 and len(vl2)>=10:
                obv_vals=[0]
                for i in range(1,min(len(C_),len(vl2))):
                    v = vl2[i] or 0
                    if C_[i] > C_[i-1]:   obv_vals.append(obv_vals[-1]+v)
                    elif C_[i] < C_[i-1]: obv_vals.append(obv_vals[-1]-v)
                    else:                  obv_vals.append(obv_vals[-1])
                obv = obv_vals[-1]
                obv_ma = statistics.mean(obv_vals[-10:])
                obv_trend = "UP" if obv > obv_ma else "DOWN"
        except: pass

        # Williams %R (14)
        willr=None
        if len(C_)>=14 and len(H_)>=14 and len(L_)>=14:
            hi14=max(H_[-14:]); lo14=min(L_[-14:])
            if hi14 != lo14:
                willr = round(-100*(hi14-price)/(hi14-lo14), 1)

        # CCI (20)
        cci=None
        if len(C_)>=20 and len(H_)>=20 and len(L_)>=20:
            tp_list=[(C_[i]+H_[i]+L_[i])/3 for i in range(len(C_))]
            tp20=tp_list[-20:]; tp_m=statistics.mean(tp20)
            md=statistics.mean([abs(x-tp_m) for x in tp20])
            cci=round((tp_list[-1]-tp_m)/(0.015*md), 1) if md else None

        # Pivot Points (Classic Daily)
        pivot=pp_r1=pp_r2=pp_s1=pp_s2=None
        if high and low and prev:
            pivot = round((high+low+prev)/3, 4)
            pp_r1 = round(2*pivot-low, 4)
            pp_r2 = round(pivot+(high-low), 4)
            pp_s1 = round(2*pivot-high, 4)
            pp_s2 = round(pivot-(high-low), 4)

        # Support & Resistance (swing)
        sup  = min(L_[-60:]) if len(L_)>=5 else None
        res2 = max(H_[-60:]) if len(H_)>=5 else None

        # Volume MA
        vol_avg = None
        try:
            q   = res.get("indicators",{}).get("quote",[{}])[0]
            vl  = [x for x in q.get("volume",[]) if x]
            vol_avg = int(statistics.mean(vl[-20:])) if len(vl)>=20 else None
        except: pass

        # Candle Pattern (last 3 bars)
        candle_pattern = "─"
        if len(C_)>=3 and len(H_)>=3 and len(L_)>=3:
            O_=q.get("open",[])
            O_=[x for x in O_ if x]
            if len(O_)>=3:
                o,c,h,l   = O_[-1],C_[-1],H_[-1],L_[-1]
                o2,c2     = O_[-2],C_[-2]
                body      = abs(c-o); rng=h-l or 0.0001
                # Hammer / Shooting Star
                lower_shadow = o-l if c>o else c-l
                upper_shadow = h-c if c>o else h-o
                if lower_shadow > 2*body and upper_shadow < body and body/rng>0.1:
                    candle_pattern = "🔨 HAMMER"
                elif upper_shadow > 2*body and lower_shadow < body and body/rng>0.1:
                    candle_pattern = "💫 SHOOT STAR"
                # Engulfing
                elif c>o and c2<o2 and c>o2 and o<c2:
                    candle_pattern = "🟢 BULL ENGULF"
                elif c<o and c2>o2 and c<o2 and o>c2:
                    candle_pattern = "🔴 BEAR ENGULF"
                # Doji
                elif body/rng < 0.05:
                    candle_pattern = "✚ DOJI"
                # Inside Bar
                elif h<=H_[-2] and l>=L_[-2]:
                    candle_pattern = "⬜ INSIDE BAR"

        return dict(price=price, prev=prev, high=high, low=low, vol=vol,
                    vol_avg=vol_avg, ma5=ma5, ma20=ma20, ma50=ma50,
                    ema9=ema9, ema21=ema21, ema50=ema50,
                    rsi=rsi, rsi7=rsi7,
                    bbu=bbu, bbm=bbm, bbl=bbl,
                    bb_width=bb_width, bb_pct=bb_pct,
                    atr=atr, macd_line=macd_line,
                    macd_sig=macd_sig, macd_hist=macd_hist,
                    stoch_k=stoch_k, stoch_d=stoch_d,
                    obv=obv, obv_trend=obv_trend,
                    willr=willr, cci=cci,
                    pivot=pivot, pp_r1=pp_r1, pp_r2=pp_r2,
                    pp_s1=pp_s1, pp_s2=pp_s2,
                    sup=sup, res=res2,
                    candle=candle_pattern, ok=True)
    except:
        return dict(ok=False)

# ══════════════════════════════════════════════════════════════════════
#  SCORING — Professional Multi-Factor Signal Engine v2.0
#  Factors : Momentum · RSI(14) · RSI(7) · BB · MA · EMA · MACD
#            Stochastic · Volume · OBV · Williams%R · CCI
#            Candle Pattern · Pivot · Conviction
# ══════════════════════════════════════════════════════════════════════
def sinyal(d, stars="★★★"):
    price   = d["price"]; prev = d["prev"] or price
    dp      = ((price-prev)/prev*100) if prev else 0
    rsi     = d.get("rsi");     rsi7    = d.get("rsi7")
    ma5     = d.get("ma5");     ma20    = d.get("ma20");   ma50   = d.get("ma50")
    ema9    = d.get("ema9");    ema21   = d.get("ema21");  ema50  = d.get("ema50")
    bbl     = d.get("bbl");     bbu     = d.get("bbu");    bbm    = d.get("bbm")
    bb_pct  = d.get("bb_pct")
    vol     = d.get("vol");     vol_avg = d.get("vol_avg")
    macd_l  = d.get("macd_line"); macd_s = d.get("macd_sig"); macd_h = d.get("macd_hist")
    stoch_k = d.get("stoch_k"); stoch_d = d.get("stoch_d")
    obv_tr  = d.get("obv_trend")
    willr   = d.get("willr");   cci     = d.get("cci")
    candle  = d.get("candle","─")
    sc = 0
    reasons = []

    # ── 1. MOMENTUM / PRICE ACTION (max +4 / min -4) ──────────────
    if   dp >= 5.0:  sc += 4; reasons.append(f"Momentum kuat +{dp:.1f}%")
    elif dp >= 3.0:  sc += 3; reasons.append(f"Momentum +{dp:.1f}%")
    elif dp >= 1.2:  sc += 2; reasons.append(f"Naik +{dp:.1f}%")
    elif dp >= 0.5:  sc += 1; reasons.append(f"Positif +{dp:.1f}%")
    elif dp <= -7.0: sc -= 4; reasons.append(f"Jual panic {dp:.1f}%")
    elif dp <= -5.0: sc -= 3; reasons.append(f"Turun tajam {dp:.1f}%")
    elif dp <= -2.0: sc -= 2; reasons.append(f"Melemah {dp:.1f}%")
    elif dp <= -0.5: sc -= 1; reasons.append(f"Sedikit turun {dp:.1f}%")

    # ── 2. RSI-14 (max +4 / min -3) ───────────────────────────────
    if rsi is not None:
        if   rsi <= 20: sc += 4; reasons.append(f"RSI14 sangat oversold {rsi}")
        elif rsi <= 28: sc += 3; reasons.append(f"RSI14 oversold {rsi}")
        elif rsi <= 38: sc += 2; reasons.append(f"RSI14 mendekati oversold {rsi}")
        elif rsi <= 45: sc += 1; reasons.append(f"RSI14 lemah {rsi}")
        elif rsi >= 82: sc -= 3; reasons.append(f"RSI14 sangat overbought {rsi}")
        elif rsi >= 72: sc -= 2; reasons.append(f"RSI14 overbought {rsi}")
        elif rsi >= 62: sc -= 1; reasons.append(f"RSI14 tinggi {rsi}")

    # ── 3. RSI-7 Short Term Confirmation (max +2 / min -2) ────────
    if rsi7 is not None:
        if   rsi7 <= 20: sc += 2; reasons.append(f"RSI7 extreme oversold {rsi7}")
        elif rsi7 <= 30: sc += 1; reasons.append(f"RSI7 oversold {rsi7}")
        elif rsi7 >= 80: sc -= 2; reasons.append(f"RSI7 extreme overbought {rsi7}")
        elif rsi7 >= 70: sc -= 1; reasons.append(f"RSI7 overbought {rsi7}")

    # ── 4. BOLLINGER BANDS (max +3 / min -2) ──────────────────────
    if bbl and bbu and price:
        if   price <= bbl * 0.995: sc += 3; reasons.append("Harga di bawah lower BB ← squeeze buy")
        elif price <= bbl * 1.008: sc += 2; reasons.append("Harga menyentuh lower BB")
        elif price >= bbu * 1.005: sc -= 2; reasons.append("Harga di atas upper BB ← overbought")
        elif price >= bbu * 0.992: sc -= 1; reasons.append("Harga mendekati upper BB")
        # BB %B position
        if bb_pct is not None:
            if   bb_pct <= 5:  sc += 1; reasons.append(f"BB%B sangat rendah {bb_pct:.0f}%")
            elif bb_pct >= 95: sc -= 1; reasons.append(f"BB%B sangat tinggi {bb_pct:.0f}%")

    # ── 5. MA CROSSOVER — Golden/Death Cross (max +3 / min -3) ────
    if ma5 and ma20:
        if   ma5 > ma20 * 1.015: sc += 3; reasons.append("Golden Cross kuat MA5>MA20")
        elif ma5 > ma20 * 1.005: sc += 2; reasons.append("MA5 > MA20 bullish")
        elif ma5 > ma20 * 1.001: sc += 1; reasons.append("MA5 baru melewati MA20")
        elif ma5 < ma20 * 0.985: sc -= 3; reasons.append("Death Cross MA5<MA20")
        elif ma5 < ma20 * 0.995: sc -= 2; reasons.append("MA5 < MA20 bearish")
        elif ma5 < ma20 * 0.999: sc -= 1; reasons.append("MA5 mendekati Death Cross")

    # MA50 Trend Filter
    if ma50 and price:
        if   price > ma50 * 1.02: sc += 1; reasons.append("Harga di atas MA50 uptrend")
        elif price < ma50 * 0.98: sc -= 1; reasons.append("Harga di bawah MA50 downtrend")

    # ── 6. EMA SYSTEM (max +2 / min -2) ───────────────────────────
    if ema9 and ema21:
        if   ema9 > ema21 * 1.01: sc += 2; reasons.append("EMA9 > EMA21 bull trend")
        elif ema9 > ema21:        sc += 1; reasons.append("EMA9 melewati EMA21")
        elif ema9 < ema21 * 0.99: sc -= 2; reasons.append("EMA9 < EMA21 bear trend")
        elif ema9 < ema21:        sc -= 1; reasons.append("EMA9 di bawah EMA21")

    # ── 7. MACD (max +3 / min -3) ─────────────────────────────────
    if macd_l is not None and macd_s is not None:
        if   macd_l > macd_s and macd_l > 0:   sc += 3; reasons.append("MACD bullish above zero")
        elif macd_l > macd_s and macd_l <= 0:  sc += 2; reasons.append("MACD cross signal bullish")
        elif macd_l > 0 and macd_l > macd_s*0.9: sc += 1; reasons.append("MACD positif")
        elif macd_l < macd_s and macd_l < 0:   sc -= 3; reasons.append("MACD bearish below zero")
        elif macd_l < macd_s:                   sc -= 2; reasons.append("MACD cross signal bearish")
    if macd_h is not None:
        if   macd_h > 0 and macd_h > abs(macd_h)*0.2: sc += 1; reasons.append("MACD histogram positif")
        elif macd_h < 0 and abs(macd_h) > 0:           sc -= 1; reasons.append("MACD histogram negatif")

    # ── 8. STOCHASTIC %K/%D (max +3 / min -2) ─────────────────────
    if stoch_k is not None:
        if   stoch_k <= 15: sc += 3; reasons.append(f"Stoch oversold extreme {stoch_k:.0f}")
        elif stoch_k <= 25: sc += 2; reasons.append(f"Stoch oversold {stoch_k:.0f}")
        elif stoch_k <= 35: sc += 1; reasons.append(f"Stoch mendekati oversold {stoch_k:.0f}")
        elif stoch_k >= 85: sc -= 2; reasons.append(f"Stoch overbought {stoch_k:.0f}")
        elif stoch_k >= 75: sc -= 1; reasons.append(f"Stoch mendekati overbought {stoch_k:.0f}")
        # %K cross %D
        if stoch_d is not None:
            if stoch_k > stoch_d and stoch_k < 50:
                sc += 1; reasons.append("Stoch %K cross %D di zona rendah ▲")
            elif stoch_k < stoch_d and stoch_k > 50:
                sc -= 1; reasons.append("Stoch %K cross %D di zona tinggi ▼")

    # ── 9. VOLUME SURGE (max +3 / min -1) ─────────────────────────
    if vol and vol_avg and vol_avg > 0:
        ratio = vol / vol_avg
        if   ratio >= 4.0: sc += 3; reasons.append(f"Volume surge EXTREME {ratio:.1f}x avg")
        elif ratio >= 2.5: sc += 2; reasons.append(f"Volume surge tinggi {ratio:.1f}x avg")
        elif ratio >= 1.5: sc += 1; reasons.append(f"Volume di atas rata-rata {ratio:.1f}x")
        elif ratio <= 0.3: sc -= 1; reasons.append(f"Volume sangat sepi {ratio:.1f}x avg")

    # ── 10. OBV TREND (max +2 / min -2) ───────────────────────────
    if obv_tr == "UP":   sc += 2; reasons.append("OBV trending UP ← akumulasi")
    elif obv_tr == "DOWN": sc -= 2; reasons.append("OBV trending DOWN ← distribusi")

    # ── 11. WILLIAMS %R (max +2 / min -2) ─────────────────────────
    if willr is not None:
        if   willr <= -90: sc += 2; reasons.append(f"Williams%R oversold extreme {willr}")
        elif willr <= -80: sc += 1; reasons.append(f"Williams%R oversold {willr}")
        elif willr >= -10: sc -= 2; reasons.append(f"Williams%R overbought {willr}")
        elif willr >= -20: sc -= 1; reasons.append(f"Williams%R overbought zone {willr}")

    # ── 12. CCI (max +2 / min -2) ─────────────────────────────────
    if cci is not None:
        if   cci <= -200: sc += 2; reasons.append(f"CCI extreme oversold {cci:.0f}")
        elif cci <= -100: sc += 1; reasons.append(f"CCI oversold {cci:.0f}")
        elif cci >= 200:  sc -= 2; reasons.append(f"CCI extreme overbought {cci:.0f}")
        elif cci >= 100:  sc -= 1; reasons.append(f"CCI overbought {cci:.0f}")

    # ── 13. CANDLE PATTERN (max +2 / min -2) ──────────────────────
    if "HAMMER"     in candle: sc += 2; reasons.append(f"Candle: {candle}")
    if "BULL ENGULF"in candle: sc += 2; reasons.append(f"Candle: {candle}")
    if "DOJI"       in candle: sc += 1; reasons.append(f"Candle: {candle} ← reversal?")
    if "INSIDE BAR" in candle: sc += 1; reasons.append(f"Candle: {candle} ← breakout pending")
    if "SHOOT STAR" in candle: sc -= 2; reasons.append(f"Candle: {candle} ← topping signal")
    if "BEAR ENGULF"in candle: sc -= 2; reasons.append(f"Candle: {candle}")

    # ── 14. CONVICTION BONUS (max +3 / min -1) ────────────────────
    n = stars.count("★")
    if   n >= 5: sc += 3; reasons.append("Conviction ★★★★★ Highest")
    elif n >= 4: sc += 2; reasons.append("Conviction ★★★★ High")
    elif n >= 3: sc += 1; reasons.append("Conviction ★★★ Moderate")
    elif n <= 2: sc -= 1; reasons.append("Conviction rendah ★★")

    # ── SIGNAL OUTPUT ──────────────────────────────────────────────
    if   sc >= 14: sig = "💎 STRONG BUY ▲▲▲"; col = G
    elif sc >= 10: sig = "🟢 BUY        ▲▲ "; col = G
    elif sc >=  6: sig = "📈 AKUMULASI  ▲  "; col = C
    elif sc >=  3: sig = "⚪ HOLD       ─  "; col = Y
    elif sc >=  1: sig = "🟡 NEUTRAL    ─  "; col = Y
    elif sc >= -2: sig = "⏳ WAIT/WATCH ↓  "; col = Y
    elif sc >= -5: sig = "🔴 REDUCE     ▼  "; col = R
    else:          sig = "💀 SELL/EXIT  ▼▼▼"; col = R

    return sig, col, sc, reasons

# ══════════════════════════════════════════════════════════════════════
#  ZONA HARGA — Entry / TP / SL  +  Pivot Points
# ══════════════════════════════════════════════════════════════════════
def zona(d):
    p    = d["price"]
    atr  = d.get("atr")  or p * 0.025
    sup  = d.get("sup")  or p * 0.93
    bbl  = d.get("bbl")  or p * 0.97
    ma20 = d.get("ma20") or p
    pp_s1= d.get("pp_s1")
    pp_r1= d.get("pp_r1")
    pivot= d.get("pivot")

    # Entry: best confluence support
    candidates = [x for x in [sup, bbl, ma20, pp_s1] if x and x > 0]
    ei   = round(min(candidates) * 1.003, 4) if candidates else round(p * 0.98, 4)
    sl   = round(max(sup * 0.965, p - 1.8*atr), 4)
    risk = abs(p - sl) or atr
    tp1  = round(p + 1.5*risk, 4)
    tp2  = round(p + 2.5*risk, 4)
    tp3  = round(p + 4.0*risk, 4)
    tp4  = round(p + 6.0*risk, 4)  # Extended target
    rr   = round(abs(tp2-p)/risk, 2) if risk else 0
    pnl1 = round((tp1-p)/p*100, 1)
    pnl2 = round((tp2-p)/p*100, 1)
    pnl3 = round((tp3-p)/p*100, 1)
    pnl4 = round((tp4-p)/p*100, 1)
    return dict(ei=ei, sl=sl, tp1=tp1, tp2=tp2, tp3=tp3, tp4=tp4,
                pivot=pivot, pp_r1=pp_r1, pp_s1=pp_s1,
                rr=rr, pnl1=pnl1, pnl2=pnl2, pnl3=pnl3, pnl4=pnl4)

# ══════════════════════════════════════════════════════════════════════
#  MAIN
# ══════════════════════════════════════════════════════════════════════
def main():
    clr()
    print(f"\n{B}{C}  ▶  ASX Professional Screening — Mengambil data pasar...{RS}\n")

    fetched = {}
    for i, item in enumerate(watchlist, 1):
        pct = int(i / len(watchlist) * 32)
        bar = "█"*pct + "░"*(32-pct)
        sys.stdout.write(f"\r  [{bar}] {item['n']:<6}  {i}/{len(watchlist)}")
        sys.stdout.flush()
        fetched[item["s"]] = fetch(item["s"])
        time.sleep(0.22)

    clr()
    now = datetime.now().strftime("%d %b %Y  %H:%M WIB")
    W2 = 79

    # Header compact
    print(f"\n{B}{C}{'═'*W2}{RS}")
    print(f"{B}{C} ASX PRO SCREENING  v9.0  {RS}")
    print(f"{B}{C} Coal·Iron·Li·RE·Cu·Energy·U·Gold{RS}")
    print(f" Filter: < AUD${HARGA_MAKS}  |  {now}")
    print(f"{B}{C}{'═'*W2}{RS}")

    results = []
    cur     = None
    skipped = 0

    sort_key = lambda x: (
        SECTOR_ORDER.index(x["sector"])
        if x["sector"] in SECTOR_ORDER else 99
    )

    for item in sorted(watchlist, key=sort_key):
        d = fetched.get(item["s"], {"ok": False})
        if not d.get("ok"):
            skipped += 1
            continue

        price = d["price"]
        if price <= 0 or price > HARGA_MAKS:
            skipped += 1
            continue

        dp  = ((price-(d["prev"] or price))/(d["prev"] or price)*100) if d["prev"] else 0
        sig, scol, score, reasons = sinyal(d, item.get("stars","★★★"))
        z   = zona(d)
        rsi = d.get("rsi"); rsi7 = d.get("rsi7")
        stoch_k = d.get("stoch_k"); stoch_d = d.get("stoch_d")
        macd_h  = d.get("macd_hist"); macd_l = d.get("macd_line")
        willr   = d.get("willr");    cci     = d.get("cci")
        obv_tr  = d.get("obv_trend","─")
        candle  = d.get("candle","─")
        bb_pct  = d.get("bb_pct")

        # Sektor Header compact
        if item["sector"] != cur:
            cur = item["sector"]
            sec_label = cur.replace("ENERGY ★★★★★","ENERGY T1 ★★★★★")\
                           .replace("ENERGY ★★★★","ENERGY T2 ★★★★")\
                           .replace("ENERGY ★★★","ENERGY T3 ★★★")\
                           .replace("ENERGY ★★","ENERGY T4 ★★")
            print(f"\n{B}{M}══ {sec_label} ══{RS}")

        # RSI-14 color
        if rsi is not None:
            rc = R if rsi>=70 else (G if rsi<=30 else W)
            rsi_str = f"{rc}{rsi:>5.1f}{RS}"
        else: rsi_str = "  -  "

        # RSI-7
        if rsi7 is not None:
            rc7 = R if rsi7>=70 else (G if rsi7<=30 else Y)
            rsi7_str = f"{rc7}{rsi7:>5.1f}{RS}"
        else: rsi7_str = "  -  "

        # Stochastic
        if stoch_k is not None:
            sc2 = R if stoch_k>=80 else (G if stoch_k<=20 else W)
            stoch_str = f"{sc2}%K{stoch_k:>5.1f}{RS}"
            if stoch_d: stoch_str += f" %D{stoch_d:>5.1f}"
        else: stoch_str = "   -  "

        # MACD
        if macd_h is not None:
            mc = G if macd_h > 0 else R
            macd_str = f"{mc}hist:{macd_h:>+.4f}{RS}"
        elif macd_l is not None:
            mc = G if macd_l > 0 else R
            macd_str = f"{mc}line:{macd_l:>+.4f}{RS}"
        else: macd_str = "   -  "

        # Williams %R
        if willr is not None:
            wc = G if willr <= -80 else (R if willr >= -20 else W)
            willr_str = f"{wc}W%R:{willr:>6.1f}{RS}"
        else: willr_str = "      -"

        # CCI
        if cci is not None:
            cc2 = G if cci <= -100 else (R if cci >= 100 else W)
            cci_str = f"{cc2}CCI:{cci:>7.1f}{RS}"
        else: cci_str = "       -"

        # OBV
        obv_col = G if obv_tr=="UP" else (R if obv_tr=="DOWN" else DM)
        obv_str = f"{obv_col}OBV:{obv_tr or '─':>4}{RS}"

        # BB %B
        if bb_pct is not None:
            bc = G if bb_pct<=15 else (R if bb_pct>=85 else W)
            bb_str = f"{bc}BB%B:{bb_pct:>5.1f}%{RS}"
        else: bb_str = "        -"

        # MA Trend
        ma_str = "-"
        if d.get("ma5") and d.get("ma20"):
            if d["ma5"] > d["ma20"] * 1.005:   ma_str = f"{G}▲ NAIK{RS}"
            elif d["ma5"] < d["ma20"] * 0.995: ma_str = f"{R}▼ TURUN{RS}"
            else:                               ma_str = f"{Y}─ SIDEWAYS{RS}"

        # EMA Trend
        ema_str = "-"
        if d.get("ema9") and d.get("ema21"):
            if d["ema9"] > d["ema21"]:   ema_str = f"{G}EMA9>21▲{RS}"
            else:                         ema_str = f"{R}EMA9<21▼{RS}"

        # Volume
        vol_str = fvol(d.get("vol"))
        if d.get("vol") and d.get("vol_avg") and d["vol_avg"] > 0:
            ratio = d["vol"] / d["vol_avg"]
            vc = G if ratio>=2 else (Y if ratio>=1.3 else DM)
            vol_str += f" {vc}({ratio:.1f}x){RS}"

        stars_disp = star_color(item.get("stars","★★★"))
        W2 = 79  # mobile width

        # RSI-14
        if rsi is not None:
            rc = R if rsi>=70 else (G if rsi<=30 else W)
            rsi_str = f"{rc}{rsi:.1f}{RS}"
        else: rsi_str = "-"

        # RSI-7
        if rsi7 is not None:
            rc7 = R if rsi7>=70 else (G if rsi7<=30 else Y)
            rsi7_str = f"{rc7}{rsi7:.1f}{RS}"
        else: rsi7_str = "-"

        # Stochastic
        if stoch_k is not None:
            sc2 = R if stoch_k>=80 else (G if stoch_k<=20 else W)
            stoch_str = f"{sc2}{stoch_k:.0f}{RS}"
            if stoch_d: stoch_str += f"/{stoch_d:.0f}"
        else: stoch_str = "-"

        # MACD
        if macd_h is not None:
            mc = G if macd_h > 0 else R
            macd_str = f"{mc}{macd_h:+.4f}{RS}"
        elif macd_l is not None:
            mc = G if macd_l > 0 else R
            macd_str = f"{mc}{macd_l:+.4f}{RS}"
        else: macd_str = "-"

        # Williams %R
        if willr is not None:
            wc = G if willr<=-80 else (R if willr>=-20 else W)
            willr_str = f"{wc}{willr:.0f}{RS}"
        else: willr_str = "-"

        # CCI
        if cci is not None:
            cc2 = G if cci<=-100 else (R if cci>=100 else W)
            cci_str = f"{cc2}{cci:.0f}{RS}"
        else: cci_str = "-"

        # OBV
        obv_col = G if obv_tr=="UP" else (R if obv_tr=="DOWN" else DM)
        obv_str = f"{obv_col}{obv_tr or '─'}{RS}"

        # BB %B
        if bb_pct is not None:
            bc = G if bb_pct<=15 else (R if bb_pct>=85 else W)
            bb_str = f"{bc}{bb_pct:.0f}%{RS}"
        else: bb_str = "-"

        # MA Trend
        if d.get("ma5") and d.get("ma20"):
            if d["ma5"] > d["ma20"]*1.005:   ma_str = f"{G}▲{RS}"
            elif d["ma5"] < d["ma20"]*0.995: ma_str = f"{R}▼{RS}"
            else:                             ma_str = f"{Y}─{RS}"
        else: ma_str = "─"

        # EMA
        if d.get("ema9") and d.get("ema21"):
            ema_str = f"{G}▲{RS}" if d["ema9"]>d["ema21"] else f"{R}▼{RS}"
        else: ema_str = "─"

        # Volume
        vol_str = fvol(d.get("vol"))
        if d.get("vol") and d.get("vol_avg") and d["vol_avg"]>0:
            ratio = d["vol"]/d["vol_avg"]
            vc = G if ratio>=2 else (Y if ratio>=1.3 else DM)
            vol_str += f"{vc}({ratio:.1f}x){RS}"

        # Score bar compact (15 chars)
        score_bar_len = min(max(score+8, 0), 15)
        score_bar = "█"*score_bar_len + "░"*(15-score_bar_len)
        score_col = G if score>=6 else (R if score<=-3 else Y)

        # Top reason (1 only for mobile)
        reason1 = reasons[0][:73] if reasons else "─"

        # ── MOBILE DISPLAY 79 cols ──────────────────────────────
        W2 = 79
        print(f"\n{B}{C}{'─'*W2}{RS}")
        print(f" {B}{W}{item['n']:<5}{RS} {stars_disp} {cpct(dp)}  ${fp(price)}  H:{G}${fp(d.get('high'))}{RS} L:{R}${fp(d.get('low'))}{RS}")
        print(f" RSI:{rsi_str}  R7:{rsi7_str}  St:{stoch_str}  MA:{ma_str}  EMA:{ema_str}  OBV:{obv_str}")
        print(f" MACD:{macd_str}  W%R:{willr_str}  CCI:{cci_str}  BB:{bb_str}  VOL:{vol_str}")
        if candle != "─": print(f" {candle}")
        print(f" EN:{Y}${fp(z['ei'])}{RS}  SL:{R}${fp(z['sl'])}{RS}  RR:{B}1:{z['rr']}{RS}  TP1:{G}+{z['pnl1']}%{RS}  TP2:{G}+{z['pnl2']}%{RS}  TP3:{G}+{z['pnl3']}%{RS}")
        print(f" {score_col}[{score_bar}]{score:+d}{RS}  {scol}{B}{sig}{RS}")
        print(f" {DM}{reason1[:75]}{RS}")

        results.append({
            "n":item["n"], "sector":item["sector"],
            "price":price, "dp":dp, "sig":sig, "rsi":rsi,
            "stars":item.get("stars","★"), "note":item["note"],
            "catalyst":item.get("catalyst","-"),
            "pnl2":z["pnl2"], "rr":z["rr"], "score":score,
            "stoch_k":stoch_k, "macd_h":macd_h, "obv_tr":obv_tr
        })

    # ── RINGKASAN ─────────────────────────────────────────────────
    print(f"\n{B}{C}{'═'*W2}{RS}")
    print(f"{B}{C} RINGKASAN — JP MORGAN REPORT{RS}")
    print(f"{'═'*W2}")
    print(f" Lolos filter : {B}{W}{len(results)}{RS} saham  Skip:{DM}{skipped}{RS}")

    # Top Picks
    buy_list = [r for r in results if "BUY" in r["sig"] or "AKUMULASI" in r["sig"]]
    if buy_list:
        sorted_buy = sorted(buy_list, key=lambda x: (x.get("score",0), x["stars"].count("★")), reverse=True)
        print(f"\n{G}{B} ━ TOP PICKS (BUY/AKUMULASI) ━{RS}")
        print(f" {'Kode':<5} {'★':^5} {'$':>6} {'Dy%':>6} {'R14':>4} {'Sc':>4}")
        print(f" {'─'*W2}")
        for r in sorted_buy[:10]:
            sc_col = G if r.get("score",0)>=6 else Y
            r14 = f"{r['rsi']:.0f}" if r['rsi'] else "-"
            print(f" {G}{r['n']:<5}{RS} {r['stars']:^5} ${fp(r['price']):>5}"
                  f" {cpct(r['dp'])} {r14:>4}"
                  f" {sc_col}{r.get('score',0):>+3d}{RS}"
                  f"  {G}TP2+{r['pnl2']}%{RS}")

    # Oversold Watch
    oversold = [r for r in results if r["rsi"] and r["rsi"] <= 35]
    if oversold:
        print(f"\n{Y}{B} ━ OVERSOLD RSI≤35 (Akumulasi) ━{RS}")
        for r in sorted(oversold, key=lambda x: x["rsi"]):
            r14 = f"{r['rsi']:.0f}" if r['rsi'] else "-"
            print(f" {Y}◆{r['n']:<5}{RS} RSI:{G}{r14}{RS} ${fp(r['price'])} {cpct(r['dp'])}")

    # Energy
    energy_list = [r for r in results if "ENERGY" in r["sector"]]
    if energy_list:
        print(f"\n{OR}{B} ━ ENERGY OIL & GAS 2026 ━{RS}")
        for r in sorted(energy_list, key=lambda x: x["stars"].count("★"), reverse=True):
            print(f" {OR}▶{r['n']:<5}{RS} {r['stars']:^5} ${fp(r['price'])} {cpct(r['dp'])}")

    # Gainer / Loser
    valid = [r for r in results if r["dp"] is not None]
    if valid:
        best  = max(valid, key=lambda x: x["dp"])
        worst = min(valid, key=lambda x: x["dp"])
        print(f"\n {G}▲ GAINER: {best['n']}  ${fp(best['price'])}  {cpct(best['dp'])}{RS}")
        print(f" {R}▼ LOSER : {worst['n']}  ${fp(worst['price'])}  {cpct(worst['dp'])}{RS}")

    print(f"\n{B}{C}{'═'*W2}{RS}")
    print(f" {G}✔ {now}{RS}")
    print(f" python screening_asx.py")
    print(f" {DM}⚠ Bukan saran investasi. DYOR.{RS}")
    print(f"{B}{C}{'═'*W2}{RS}\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n  {Y}Keluar. Sampai jumpa! 👋{RS}\n")
