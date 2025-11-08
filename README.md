# TD02_Bitcoin_Wallet_Practice  
### by Jennifer El Achkar (BIP-39 & BIP-32)
---

## Table of contents
1. Version Française
   - Objectif
   - Installation
   - Structure du projet
   - Exemples d’utilisation
   - Tests & Vérification
   - Avertissement
   - Références
2. English Version


---
---

## Version Française  
*(For English version, please see below)*

---

## Objectif  
Mettre en œuvre un générateur mnémonique conforme à la norme **BIP-39**, ainsi qu’une dérivation de clés déterministes **BIP-32**, entièrement reproductibles en ligne de commande, **sans utiliser de bibliothèques Bitcoin précompilées**.

### Installation
```bash
git clone https://github.com/Jenniferachkar/TD02_Bitcoin_Wallet_practice.git
cd TD02_Bitcoin_Wallet_practice
source .venv/bin/activate       # macOS / Linux
.\.venv\Scripts\activate        # Windows (PowerShell)
pip install -r requirements.txt
cd scripts
```
<img width="1979" height="296" alt="image" src="https://github.com/user-attachments/assets/50c80524-ba67-4c3e-9326-aafaf67528c0" />
<img width="2298" height="489" alt="image" src="https://github.com/user-attachments/assets/e91c1028-3a86-4510-839c-c9320c547e6c" />


### Structure du projet
```vbnet
TD02_Bitcoin_Wallet_practice/
	scripts
			bip39.py        # génération / import / validation de mnémonique
			bip32.py        # master key, dérivations child
			main.py         # CLI interactive
			bip39_english.txt    # BIP-39 English liste de mots (2048 mots)
	README.md
```

### Exemple d'utilisation
```vbnet
=== BITCOIN WALLET TOOL ===
1. Generate new wallet
2. Import existing mnemonic
Choose option (1 or 2): 1

Enter entropy size (128/192/256): 128
Mnemonic:
abandon abandon ... about

Seed (hex): 5eb00bb... 
Master Private Key: 9a6e...
Master Chain Code:  54b1...
Master Public Key:  02d3...

Child (m/0) Private Key: ...
Child (m/0) Chain Code: ...
```
<img width="2300" height="1121" alt="image" src="https://github.com/user-attachments/assets/e27a999c-ca59-4f38-bc62-89f6202c308b" />
<img width="1782" height="536" alt="image" src="https://github.com/user-attachments/assets/0155a603-162b-4493-81cf-5902beaf2504" />



### Tests & Vérification
Vérifier la seed sur : https://iancoleman.io/bip39/
 (coller le seed hex ou la phrase mnémonique)
 
Commandes utiles :
```bash
pip install pytest
pytest
```
### Avertissement

Ce projet est pédagogique. Ne pas utiliser ces clés pour des fonds réels. 
**Il ne faut jamais partager sa propre clé privée**.

### Références

BIP-39: Mnemonic Code for Generating Deterministic Keys — https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki                                   
BIP-32: Hierarchical Deterministic Wallets — https://github.com/bitcoin/bips/blob/master/bip-0032.mediawiki                                                
Ian Coleman’s BIP39 Tool — https://iancoleman.io/bip39/

---

## English version

---

## Objective  
Implement a mnemonic generator compliant with the **BIP-39** standard, as well as a deterministic key derivation system based on **BIP-32**, fully reproducible from the command line, **without using precompiled Bitcoin libraries**.

### Installation
```bash
git clone https://github.com/Jenniferachkar/TD02_Bitcoin_Wallet_practice.git
cd TD02_Bitcoin_Wallet_Practice
source .venv/bin/activate       # macOS / Linux
.\.venv\Scripts\activate        # Windows (PowerShell)
pip install -r requirements.txt
cd scripts
```
<img width="1979" height="296" alt="image" src="https://github.com/user-attachments/assets/50c80524-ba67-4c3e-9326-aafaf67528c0" />
<img width="2298" height="489" alt="image" src="https://github.com/user-attachments/assets/e91c1028-3a86-4510-839c-c9320c547e6c" />

### Project Structure
```vbnet
TD02_Bitcoin_Wallet_Practice/
    scripts
        bip39.py              # generation / import / validation of mnemonic
        bip32.py              # master key, child derivations
        main.py               # interactive CLI
        bip39_english.txt     # BIP-39 English word list (2048 words)
    README.md
```
### Example of use
```vbnet
=== BITCOIN WALLET TOOL ===
1. Generate new wallet
2. Import existing mnemonic
Choose option (1 or 2): 1

Enter entropy size (128/192/256): 128
Mnemonic:
abandon abandon ... about

Seed (hex): 5eb00bb... 
Master Private Key: 9a6e...
Master Chain Code:  54b1...
Master Public Key:  02d3...

Child (m/0) Private Key: ...
Child (m/0) Chain Code: ...
```
<img width="2300" height="1121" alt="image" src="https://github.com/user-attachments/assets/e27a999c-ca59-4f38-bc62-89f6202c308b" />
<img width="1782" height="536" alt="image" src="https://github.com/user-attachments/assets/0155a603-162b-4493-81cf-5902beaf2504" />

### Tests & Verification
Verify the seed on: https://iancoleman.io/bip39/
(paste the hex seed or the mnemonic phrase)
Useful commands:
```bash
pip install pytest
pytest
```

### Warning

This project is for educational purposes only. Do not use these keys for real funds.
**Never share your private key**.

### References
BIP-39: Mnemonic Code for Generating Deterministic Keys — https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki
BIP-32: Hierarchical Deterministic Wallets — https://github.com/bitcoin/bips/blob/master/bip-0032.mediawiki
Ian Coleman’s BIP39 Tool — https://iancoleman.io/bip39/


