# fich

Suppression sécurisée et hashage.

## Introduction

Utilitaire axé sur la suppression sécurisée et le hashage de fichiers. 
Il est également possible de consulter les informations d'un fichier et
de nettoyer l'espace disque libre.

```bash
fich <action> <src> [args]
```

#### Arguments communs

* __time__ - indique d'afficher le temps mis par les opérations.

```bash
fich hash mon_fich.md --time
```

## Installation

```bash
# https://pypi.org/project/fich/
pip install fich
```

## Actions disponibles

### Supprimer

_Noms de l'action: delete, rm_

La suppression du fichier s'effectue en 3 étapes:

* On réecris sur le fichier ("niter" fois)
* On renomme le fichier (aléatoirement)
* On supprime le lien physique (unlink)

#### Arguments

* __niter__ (1) - nombre de réecriture sur le fichier.
* __blank__ - indique si la réecriture sur le fichier doit se faire avec
              des octets null. Dans le cas contraire on utilise des octets 
              aléatoirement générés.
* __only-unlink__ - indique si l'on ne supprime que le lien physique.

```bash
fich delete mon_fich.md
# Suppression "musclée"
fich delete mes_secrets.md --niter 5
# Suppression "réelle" (équivalent de la fonctionnalité de suppression du logiciel bleachbit)
fich delete mes_secrets.md --blank
# Suppression "fictive" (équivalent de la fonctionnalité de suppression de votre système)
fich delete mon_chien.jpg --only-unlink
```

---
### Hasher

_Nom de l'action: hash, h_

#### Arguments

* __hash-type__ (sha256) - algorithme de hash à utiliser.
* __digest-size__ (32) - Taille en octet du hash en sortie (valable pour blake et shake).

```bash
fich hash mon_fich.md
fich hash mon_fich.md --hash-type sha512
fich hash mon_fich.md --hash-type shake_128 --digest-size 40
```

#### Quelques algorithmes supportés

* sha224 
* sha256 
* sha384 
* sha512
* sha3_224
* sha3_256
* sha3_512

## Alias

* blake: alias pour blake2s et blake2b (choix autp en fonction de l'architecture).

Pour la liste entière (dépend de votre interpréteur python):

```bash
fich --help
```

---
### Afficher les informations

_Nom de l'action: info, inf, i_

```bash
fich info mon_fich.md
```

Cette fonctionnalité est copiée sur ```ls -l mon_fich.md```. Les différences sont:

* Inode à la place du nom.
* Taille du fichier en o, ko, mo, go.
* Pour la date de dernière modification, seule l'heure s'affiche lorsque la
  modification a eu lieu le jour même.

---
### Réecrire sur l'espace disque libre

_Nom de l'action: clean, c_

#### Arguments

* __niter__ (1) - (idem que pour delete).
* __blank__ - (idem que pour delete).

```bash
fich clean /home/me
```

