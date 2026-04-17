import numpy as np
import matplotlib.pyplot as plt

# 1. PÁLYA PARAMÉTEREK (7x10 méteres csempe)
hossz = 10.0     
szelesseg = 7.0   
felbontas = 0.05  

x = np.arange(-szelesseg/2, szelesseg/2, felbontas)
y = np.arange(0, hossz, felbontas)
X, Y = np.meshgrid(x, y)

# 2. Camber - 2.5%
Z_camber = -np.abs(X) * 0.025

# 3. KÁTYÚ GENERÁLÁSA 
katyu_x = 1.5         
katyu_y = 5.0         
katyu_melyseg = 0.08  
katyu_sugar_x = 0.4   
katyu_sugar_y = 0.6   

Z_katyu = -katyu_melyseg * np.exp(-(((X - katyu_x)**2 / katyu_sugar_x**2) + ((Y - katyu_y)**2 / katyu_sugar_y**2)))

Z_total = Z_camber + Z_katyu

print("Út mátrix legenerálva! A 3D modell betöltése...")

fig, ax = plt.subplots(subplot_kw={"projection": "3d"}, figsize=(10, 7))

surf = ax.plot_surface(X, Y, Z_total, cmap='plasma', edgecolor='none')

ax.set_title('Generált ASAM Útfelület (2.5% Camber + Kátyú)')
ax.set_xlabel('Szélesség (X) [m]')
ax.set_ylabel('Hosszúság (Y) [m]')
ax.set_zlabel('Magasság (Z) [m]')

ax.set_box_aspect((szelesseg, hossz, 1.5)) 

plt.show()

# 4. EXPORTÁLÁS OpenCRG (.crg) ASCII FORMÁTUMBA
import os
print("CRG fájl generálása tiszta Pythonnal...")

aktualis_mappa = os.path.dirname(os.path.abspath(__file__))

fajlnev = os.path.join(aktualis_mappa, 'ut_katyuval_01.crg')

u_meret = Z_total.shape[0]  
v_meret = Z_total.shape[1]  

with open(fajlnev, 'w') as f:
    # 1. OpenCRG Fejléc (Header) megírása
    f.write("*CRG DEF\n")
    f.write(f"$ B UB {0.0:.6f}\n")                     # Pálya kezdete (U)
    f.write(f"$ B UE {hossz:.6f}\n")                   # Pálya vége (U)
    f.write(f"$ B UI {felbontas:.6f}\n")               # Lépésköz hosszában (U)
    f.write(f"$ B VMIN {-szelesseg / 2.0:.6f}\n")      # Bal szél (V)
    f.write(f"$ B VMAX {szelesseg / 2.0:.6f}\n")       # Jobb szél (V)
    f.write(f"$ B VI {felbontas:.6f}\n")               # Lépésköz keresztben (V)
    f.write("*CRG DATA\n")
    
    # 2. A Magassági (Z) értékek kiírása
    # A szabvány szerint: rögzítjük az U-t, végigmegyünk a V-n, majd ugrunk a következő U-ra.
    for i in range(u_meret):
        # Egy sor (egy U pozícióhoz tartozó összes V érték) kiválasztása
        sor_ertekek = Z_total[i, :]
        # Szöveggé alakítjuk 6 tizedesjegy pontossággal, szóközzel elválasztva
        sor_szoveg = " ".join([f"{z:.6f}" for z in sor_ertekek])
        f.write(sor_szoveg + "\n")

print(f"A '{fajlnev}' sikeresen elmentve a mappádba!")