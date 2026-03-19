#!/usr/bin/env python3
"""
ADE STRATEGI HUB 2026
Jalankan: python ade_strategi_hub_2026.py
"""

import os, time, sys, statistics, requests
from datetime import datetime

portfolio = [
    {"s":"NVDA",    "n":"NVDA",  "sektor":"AI/US",    "avg":183.14, "tp":220.0,  "sl":165.0},
    {"s":"MSFT",    "n":"MSFT",  "sektor":"AI/US",    "avg":380.0,  "tp":450.0,  "sl":340.0},
    {"s":"PLTR",    "n":"PLTR",  "sektor":"AI/US",    "avg":25.0,   "tp":40.0,   "sl":18.0},
    {"s":"BRN.AX",  "n":"BRN",   "sektor":"AI/ASX",   "avg":0.04,   "tp":0.07,   "sl":0.025},
    {"s":"AI8.AX",  "n":"AI8",   "sektor":"AI/ASX",   "avg":0.08,   "tp":0.15,   "sl":0.05},
    {"s":"RDT.AX",  "n":"RDT",   "sektor":"AI/ASX",   "avg":0.10,   "tp":0.18,   "sl":0.07},
    {"s":"OD6.AX",  "n":"OD6",   "sektor":"MIN/ASX",  "avg":0.12,   "tp":0.20,   "sl":0.08},
    {"s":"RAC.AX",  "n":"RAC",   "sektor":"MIN/ASX",  "avg":1.14,   "tp":1.60,   "sl":0.90},
    {"s":"VAU.AX",  "n":"VAU",   "sektor":"MIN/ASX",  "avg":4.50,   "tp":6.00,   "sl":3.60},
    {"s":"LTR.AX",  "n":"LTR",   "sektor":"MIN/ASX",  "avg":1.69,   "tp":2.40,   "sl":1.30},
    {"s":"PLS.AX",  "n":"PLS",   "sektor":"MIN/ASX",  "avg":2.80,   "tp":4.00,   "sl":2.20},
    {"s":"IGO.AX",  "n":"IGO",   "sektor":"MIN/ASX",  "avg":4.50,   "tp":6.50,   "sl":3.50},
    {"s":"LYC.AX",  "n":"LYC",   "sektor":"MIN/ASX",  "avg":6.00,   "tp":8.50,   "sl":4.80},
    {"s":"YAL.AX",  "n":"YAL",   "sektor":"COAL/ASX", "avg":7.96,   "tp":10.00,  "sl":6.50},
    {"s":"WHC.AX",  "n":"WHC",   "sektor":"COAL/ASX", "avg":6.50,   "tp":9.00,   "sl":5.20},
    {"s":"ADRO.JK", "n":"ADRO",  "sektor":"COAL/IDX", "avg":2465.0, "tp":3000.0, "sl":2000.0},
    {"s":"BUMI.JK", "n":"BUMI",  "sektor":"COAL/IDX", "avg":150.0,  "tp":200.0,  "sl":115.0},
    {"s":"PTBA.JK", "n":"PTBA",  "sektor":"COAL/IDX", "avg":2800.0, "tp":3500.0, "sl":2300.0},
    {"s":"ANTM.JK", "n":"ANTM",  "sektor":"IHSG",     "avg":3800.0, "tp":5000.0, "sl":3000.0},
    {"s":"BBCA.JK", "n":"BBCA",  "sektor":"IHSG",     "avg":9800.0, "tp":10500.0,"sl":6200.0,
     "catatan":"⚠ Posisi rugi ~30%. TP realistis 10.500. SL 6.200."},
    {"s":"CDIA.JK", "n":"CDIA",  "sektor":"IHSG",     "avg":110.0,  "tp":160.0,  "sl":85.0},
    {"s":"PRTO.JK", "n":"PRTO",  "sektor":"IHSG",     "avg":400.0,  "tp":550.0,  "sl":320.0},
    {"s":"NINE.JK", "n":"NINE",  "sektor":"IHSG",     "avg":590.0,  "tp":850.0,  "sl":450.0},
    {"s":"GOTO.JK", "n":"GOTO",  "sektor":"IHSG",     "avg":55.0,   "tp":85.0,   "sl":40.0},
    {"s":"TLKM.JK", "n":"TLKM",  "sektor":"IHSG",     "avg":3200.0, "tp":4000.0, "sl":2700.0},
    {"s":"MEDC.JK", "n":"MEDC",  "sektor":"IHSG",     "avg":1200.0, "tp":1600.0, "sl":950.0},
    {"s":"SI=F",    "n":"SILVER","sektor":"KOMODITAS", "avg":24.0,   "tp":36.0,   "sl":28.0},
]

GOLD = {
    "harga": 4998.30,
    "avg":   2150.0,
    "sl":    4800.0,
    "tp1":   5100.0,
    "tp2":   5200.0,
    "tp3":   5400.0,
}

SEKTOR_URUTAN = ["AI/US","AI/ASX","MIN/ASX","COAL/ASX","COAL/IDX","KOMODITAS","IHSG"]

G="\033[92m"; R="\033[91m"; Y="\033[93m"; C="\033[96m"
W="\033[97m"; M="\033[95m"; DM="\033[2m"; B="\033[1m"; RS="\033[0m"

def fp(p, avg):
    if p is None or p==0: return "-"
    if avg < 0.1:  return f"{p:.4f}"
    if avg < 10:   return f"{p:.3f}"
    if avg < 500:  return f"{p:.2f}"
    return f"{p:,.0f}"

def fvol(v):
    if v is None: return "-"
    if v>=1e9: return f"{v/1e9:.1f}M"
    if v>=1e6: return f"{v/1e6:.1f}Jt"
    if v>=1e3: return f"{v/1e3:.0f}Rb"
    return str(v)

def cpct(val):
    if val is None: return "   -  "
    col = G if val>=1 else (R if val<0 else Y)
    return f"{col}{val:>+6.2f}%{RS}"

def garis(n=48): return "─"*n

def validasi(price, avg):
    if price is None or price<=0: return False
    if avg<=0: return False
    rasio = price/avg
    if rasio>200 or rasio<0.005: return False
    return True

def fetch(symbol):
    headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    urls=[
        f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?interval=5m&range=5d",
        f"https://query2.finance.yahoo.com/v8/finance/chart/{symbol}?interval=5m&range=5d",
    ]
    for url in urls:
        try:
            r=requests.get(url,headers=headers,timeout=15)
            r.raise_for_status()
            res=r.json()["chart"]["result"][0]
            meta=res["meta"]
            price=meta.get("regularMarketPrice") or meta.get("previousClose",0)
            prev=meta.get("chartPreviousClose") or meta.get("previousClose",price)
            high=meta.get("regularMarketDayHigh")
            low=meta.get("regularMarketDayLow")
            vol=meta.get("regularMarketVolume")
            currency=meta.get("currency","")
            C_=[]; H_=[]; L_=[]
            try:
                q=res.get("indicators",{}).get("quote",[{}])[0]
                C_=[x for x in q.get("close",[]) if x and x>0]
                H_=[x for x in q.get("high", []) if x and x>0]
                L_=[x for x in q.get("low",  []) if x and x>0]
            except: pass
            def ema(d,p):
                k=2/(p+1); e=[d[0]]
                for x in d[1:]: e.append(x*k+e[-1]*(1-k))
                return e
            ma5=statistics.mean(C_[-5:])  if len(C_)>=5  else None
            ma20=statistics.mean(C_[-20:]) if len(C_)>=20 else None
            rsi=None
            if len(C_)>=15:
                d=[C_[i]-C_[i-1] for i in range(1,len(C_))]
                g=sum(x for x in d[-14:] if x>0)/14
                l=sum(-x for x in d[-14:] if x<0)/14
                rsi=round(100-(100/(1+g/l)),1) if l else 100.0
            macd=sig=hist=None
            if len(C_)>=35:
                ef=ema(C_,12); es=ema(C_,26)
                ml=[f-s for f,s in zip(ef[25:],es)]
                if len(ml)>=9:
                    sl2=ema(ml,9)
                    macd=round(ml[-1],5); sig=round(sl2[-1],5)
                    hist=round(ml[-1]-sl2[-1],5)
            bbu=bbm=bbl=None
            if len(C_)>=20:
                rc=C_[-20:]; m=statistics.mean(rc); s=statistics.stdev(rc)
                bbu=round(m+2*s,4); bbm=round(m,4); bbl=round(m-2*s,4)
            atr=None
            if len(C_)>=14 and len(H_)>=14 and len(L_)>=14:
                trs=[]
                for i in range(1,min(len(C_),len(H_),len(L_))):
                    trs.append(max(H_[i]-L_[i],abs(H_[i]-C_[i-1]),abs(L_[i]-C_[i-1])))
                if len(trs)>=14: atr=round(statistics.mean(trs[-14:]),5)
            sup=min(L_[-60:]) if len(L_)>=5 else None
            res2=max(H_[-60:]) if len(H_)>=5 else None
            return dict(price=price,prev=prev,high=high,low=low,vol=vol,currency=currency,
                        ma5=ma5,ma20=ma20,rsi=rsi,macd=macd,sig=sig,hist=hist,
                        bbu=bbu,bbm=bbm,bbl=bbl,atr=atr,sup=sup,res=res2,ok=True)
        except: continue
    return dict(ok=False)

def hitung_zona(item,d):
    p=d["price"]; avg=item["avg"]
    atr=d["atr"] or p*0.02
    sup=d["sup"] or p*0.95
    bbl=d["bbl"] or p*0.97
    ma20=d["ma20"] or p
    sl_m=item.get("sl"); tp_m=item.get("tp")
    ei=round(min(sup,bbl,ma20)*1.002,5)
    en=round(p,5)
    sl=sl_m if sl_m else round(max(sup*0.97,p-1.5*atr),5)
    risk=abs(en-sl) or atr
    tp1=round(en+1.5*risk,5); tp2=round(en+2.5*risk,5); tp3=round(en+4.0*risk,5)
    if tp_m and tp_m>tp2: tp3=round(tp_m,5)
    rr=round(abs(tp2-en)/risk,2) if risk else 0
    return dict(ei=ei,en=en,sl=sl,tp1=tp1,tp2=tp2,tp3=tp3,rr=rr)

def sinyal(item,d):
    p=d["price"]; avg=item["avg"]
    prev=d["prev"] or p
    dp=((p-prev)/prev*100) if prev else 0
    tp_=((p-avg)/avg*100) if avg else 0
    rsi=d["rsi"]; ma5=d["ma5"]; ma20=d["ma20"]
    macd=d["macd"]; sg=d["sig"]; hist=d["hist"]
    bbu=d["bbu"]; bbl=d["bbl"]
    sl_m=item.get("sl"); tp_m=item.get("tp")
    sc=0; rs=[]
    if sl_m and p<=sl_m:
        return "WAJIB EXIT/CUT",f"Harga {fp(p,avg)} <= SL {fp(sl_m,avg)}",dp,tp_,"EXIT SEKARANG"
    if tp_m and p>=tp_m:
        return "TAKE PROFIT",f"Harga {fp(p,avg)} >= TP {fp(tp_m,avg)}",dp,tp_,"JUAL SEKARANG"
    if dp>=1.2:    sc+=2; rs.append(f"Harian +{dp:.1f}%")
    elif dp<=-5:   sc-=3; rs.append(f"Harian {dp:.1f}%")
    elif dp<-2:    sc-=1; rs.append(f"Harian {dp:.1f}%")
    elif dp>=0.5:  sc+=1; rs.append(f"Harian +{dp:.1f}%")
    if tp_>=15:    sc+=1; rs.append(f"Total +{tp_:.1f}%")
    elif tp_<=-15: sc-=2; rs.append(f"Total {tp_:.1f}% rugi")
    elif tp_>=5:   sc+=1; rs.append(f"Total +{tp_:.1f}%")
    elif -5<tp_<0: sc-=1; rs.append(f"Total {tp_:.1f}%")
    if rsi is not None:
        if rsi<=25:   sc+=3; rs.append(f"RSI {rsi} sangat oversold")
        elif rsi<=35: sc+=2; rs.append(f"RSI {rsi} oversold")
        elif rsi>=75: sc-=2; rs.append(f"RSI {rsi} overbought")
        elif rsi>=65: sc-=1; rs.append(f"RSI {rsi} hati-hati")
    if macd and sg:
        if macd>sg and hist and hist>0:   sc+=2; rs.append("MACD bullish")
        elif macd<sg and hist and hist<0: sc-=2; rs.append("MACD bearish")
    if bbl and p<=bbl*1.01:   sc+=2; rs.append("Di BB Lower")
    elif bbu and p>=bbu*0.99: sc-=1; rs.append("Di BB Upper")
    if ma5 and ma20:
        if ma5>ma20*1.005:   sc+=1; rs.append("MA5>MA20")
        elif ma5<ma20*0.995: sc-=1; rs.append("MA5<MA20")
    if sc>=2:
        if rsi and rsi<=35:           timing="ENTRY SEKARANG (RSI oversold)"
        elif bbl and p<=bbl*1.02:     timing="ENTRY SEKARANG (BB Lower)"
        elif macd and sg and macd>sg: timing="ENTRY SEKARANG (MACD bullish)"
        elif dp>=1.2:                 timing="ENTRY SEKARANG (momentum naik)"
        else:                         timing="TUNGGU KONFIRMASI"
    elif sc==1:  timing="CICIL SEDIKIT"
    elif sc==0:  timing="TAHAN posisi"
    else:        timing="JANGAN ENTRY dulu"
    label=("▲▲ STRONG BUY" if sc>=4 else "▲  BUY" if sc>=2 else
           "◆  AKUMULASI"  if sc==1 else "—  HOLD" if sc==0 else
           "▽  WAIT" if sc==-1 else "▼  REDUCE" if sc==-2 else "✕  SELL/EXIT")
    return label," | ".join(rs) if rs else "Data terbatas",dp,tp_,timing

def tampil_gold():
    g=GOLD
    p=g["harga"]; avg=g["avg"]
    profit=((p-avg)/avg*100)
    risk=abs(p-g["sl"])
    rr=round(abs(g["tp2"]-p)/risk,2) if risk else 0
    pc=G if profit>=0 else R
    print(f"\n  {B}{W}GOLD{RS}  {DM}[KOMODITAS] (USD/oz){RS}")
    print(f"  {garis()}")
    print(f"  {Y}⚡ Update: nano ade_strategi_hub_2026.py cari GOLD{RS}")
    print(f"  HARGA    : {B}{W}${p:,.2f}{RS}")
    print(f"  AVG BELI : {Y}${avg:,.1f}{RS}")
    print(f"  PROFIT   : {pc}{profit:+.2f}%{RS}")
    print(f"  {garis()}")
    print(f"  STOP LOSS: {R}${g['sl']:,.1f}{RS}  ⚠ wajib pasang!")
    print(f"  TP1(30%) : {G}${g['tp1']:,.1f}{RS}")
    print(f"  TP2(50%) : {G}${g['tp2']:,.1f}{RS}")
    print(f"  TP3(sisa): {G}${g['tp3']:,.1f}{RS}")
    print(f"  R:R      : {B}1 : {rr}{RS}")
    print(f"  {garis()}")
    if p>=g["tp1"]:
        print(f"  {B}{G}SINYAL : TAKE PROFIT — jual bertahap!{RS}")
    elif p<=g["sl"]:
        print(f"  {B}{R}SINYAL : WAJIB EXIT/CUT LOSS!{RS}")
    else:
        print(f"  {B}{G}SINYAL : HOLD — profit besar, jaga SL{RS}")
    print(f"  {DM}Konteks : Tren naik dari $2.150. Support $4.980-5.000{RS}")
    print(f"  {Y}Aksi    : TP1 ${g['tp1']:,.0f} jual 30% | TP2 ${g['tp2']:,.0f} jual 40% | SL ${g['sl']:,.0f}{RS}")
    print(f"  {garis()}")

def main():
    os.system("cls" if os.name=="nt" else "clear")
    print(f"\n{B}{C}  ADE STRATEGI HUB 2026 — Mengambil data...{RS}\n")
    fetched={}
    for i,item in enumerate(portfolio,1):
        pct=int(i/len(portfolio)*30)
        bar="█"*pct+"░"*(30-pct)
        sys.stdout.write(f"\r  [{bar}] {item['n']:<6} {i}/{len(portfolio)}")
        sys.stdout.flush()
        fetched[item["s"]]=fetch(item["s"])
        time.sleep(0.3)
    ok_count=sum(1 for d in fetched.values() if d.get("ok"))
    os.system("cls" if os.name=="nt" else "clear")
    now=datetime.now().strftime("%d %b %Y  %H:%M:%S")
    print(f"\n{B}{C}{'═'*50}{RS}")
    print(f"{B}{C}   ADE STRATEGI HUB 2026  —  REAL-TIME{RS}")
    print(f"   {now}  [{G}{ok_count}{RS}/{len(portfolio)} live]")
    print(f"{B}{C}{'═'*50}{RS}")
    results=[]; cur=None
    for item in sorted(portfolio,key=lambda x:SEKTOR_URUTAN.index(x["sektor"]) if x["sektor"] in SEKTOR_URUTAN else 99):
        if item["sektor"]!=cur:
            cur=item["sektor"]
            print(f"\n{B}{M}{'─'*6} {cur} {'─'*6}{RS}")
        d=fetched.get(item["s"],{"ok":False})
        if not d.get("ok"):
            print(f"\n  {B}{item['n']}{RS}  [{R}OFFLINE{RS}]")
            results.append({"n":item["n"],"rec":"OFFLINE","dp":None}); continue
        if not validasi(d["price"],item["avg"]):
            print(f"\n  {B}{item['n']}{RS}  [{Y}DATA TIDAK VALID{RS}]")
            results.append({"n":item["n"],"rec":"OFFLINE","dp":None}); continue
        rec,reason,dp,tp_,timing=sinyal(item,d)
        z=hitung_zona(item,d)
        p=d["price"]; avg=item["avg"]
        sc=G if ("BUY" in rec or "PROFIT" in rec or "AKUMULASI" in rec) else \
           R if ("EXIT" in rec or "SELL" in rec or "CUT" in rec) else Y
        tc=G if "SEKARANG" in timing else R if "JANGAN" in timing else Y
        print(f"\n  {B}{W}{item['n']}{RS}  {DM}[{item['sektor']}] ({d.get('currency','')}){RS}")
        print(f"  {garis()}")
        if item.get("catatan"): print(f"  {Y}CATATAN : {item['catatan']}{RS}")
        print(f"  HARGA    : {B}{W}{fp(p,avg)}{RS}   PREV : {fp(d['prev'],avg)}")
        print(f"  AVG BELI : {Y}{fp(avg,avg)}{RS}   VOL  : {fvol(d['vol'])}")
        h_str=f"{G}{fp(d['high'],avg)}{RS}" if d['high'] else "-"
        l_str=f"{R}{fp(d['low'],avg)}{RS}"  if d['low']  else "-"
        print(f"  HIGH/LOW : {h_str}  /  {l_str}")
        print(f"  HARIAN   : {cpct(dp)}   TOTAL : {cpct(tp_)}")
        print(f"  {garis()}")
        if d["rsi"] is not None:
            rc=R if d["rsi"]>=70 else G if d["rsi"]<=30 else W
            ket=" (Overbought!)" if d["rsi"]>=70 else " (Oversold!)" if d["rsi"]<=30 else ""
            print(f"  RSI-14   : {rc}{d['rsi']}{ket}{RS}")
        if d["macd"] is not None:
            hc=G if (d["hist"] or 0)>0 else R
            print(f"  MACD     : {hc}{d['macd']}{RS}  Sig:{d['sig']}  Hist:{hc}{d['hist']}{RS}")
        if d["bbu"]: print(f"  BB U/M/L : {R}{fp(d['bbu'],avg)}{RS}/{W}{fp(d['bbm'],avg)}{RS}/{G}{fp(d['bbl'],avg)}{RS}")
        if d["ma5"] and d["ma20"]:
            mac=G if d["ma5"]>d["ma20"] else R
            print(f"  MA 5/20  : {mac}{fp(d['ma5'],avg)}{RS} / {mac}{fp(d['ma20'],avg)}{RS}")
        if d["sup"] and d["res"]: print(f"  SUP/RES  : {G}{fp(d['sup'],avg)}{RS} / {R}{fp(d['res'],avg)}{RS}")
        print(f"  {garis()}")
        print(f"  ENTRY ID : {Y}{fp(z['ei'],avg)}{RS}")
        print(f"  ENTRY NOW: {W}{fp(z['en'],avg)}{RS}")
        print(f"  STOP LOSS: {R}{fp(z['sl'],avg)}{RS}  ⚠ wajib pasang!")
        print(f"  TP1(30%) : {G}{fp(z['tp1'],avg)}{RS}")
        print(f"  TP2(50%) : {G}{fp(z['tp2'],avg)}{RS}")
        print(f"  TP3(sisa): {G}{fp(z['tp3'],avg)}{RS}")
        print(f"  R:R      : {B}1 : {z['rr']}{RS}")
        print(f"  {garis()}")
        print(f"  {B}SINYAL : {sc}{rec}{RS}")
        print(f"  {B}TIMING : {tc}{timing}{RS}")
        print(f"  {DM}{reason}{RS}")
        print(f"  {garis()}")
        results.append({"n":item["n"],"rec":rec,"dp":dp,"tp_":tp_})
    print(f"\n{B}{M}{'─'*6} KOMODITAS {'─'*6}{RS}")
    tampil_gold()
    print(f"\n{B}{C}{'═'*50}{RS}")
    print(f"{B}{C}  RINGKASAN SINYAL{RS}")
    print(f"{B}{C}{'═'*50}{RS}")
    cats={}
    for r in results: cats[r["rec"]]=cats.get(r["rec"],0)+1
    for label,cnt in sorted(cats.items(),key=lambda x:-x[1]):
        col=G if ("BUY" in label or "PROFIT" in label or "AKUMULASI" in label) else \
            R if ("EXIT" in label or "SELL" in label or "CUT" in label or "OFFLINE" in label) else Y
        print(f"  {col}{label:<26}{RS} ({cnt}x)")
    valid=[r for r in results if r.get("dp") is not None]
    if valid:
        best=max(valid,key=lambda x:x["dp"])
        worst=min(valid,key=lambda x:x["dp"])
        print(f"\n  {G}TOP GAINER : {best['n']:<8} {cpct(best['dp'])}{RS}")
        print(f"  {R}TOP LOSER  : {worst['n']:<8} {cpct(worst['dp'])}{RS}")
        urgent=[r for r in valid if "EXIT" in r["rec"] or "CUT" in r["rec"]]
        if urgent:
            print(f"\n  {R}{B}⚠ WAJIB DIPERHATIKAN:{RS}")
            for u in urgent: print(f"  {R}  >> {u['n']}  {u['rec']}{RS}")
    print(f"\n{B}{C}{'═'*50}{RS}")
    print(f"  {G}{now}{RS}")
    print(f"  Ketik: python ade_strategi_hub_2026.py  untuk refresh")
    print(f"{B}{C}{'═'*50}{RS}\n")

if __name__=="__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n  {Y}Keluar. Sampai jumpa!{RS}\n")
