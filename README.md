# Jméno projektu (iOS)

![Bitrise](https://img.shields.io/bitrise/appid.svg?token=apptoken)
![Swift 5.0](https://img.shields.io/badge/Swift-5.0-brightgreen.svg)
![Xcode 10.2](https://img.shields.io/badge/Xcode-10.2-brightgreen.svg)
![CocoaPods 1.7](https://img.shields.io/badge/CocoaPods-1.7-brightgreen.svg)
![Fastlane](https://img.shields.io/badge/Fastlane-test,enterprise,beta-brightgreen.svg)

Při vývoji aplikace dodržujeme **GIT flow**, každý task v JIRA má svoji branch na Gitu, který ve jméně obsahuje ID tasku, aby se dalo spárovat s JIRA. V branch *master* jsou pouze releasnuté verze. Pull requesty se mergují do *develop*, kde je aktuální fungující vývojová verze aplikace. Nástroj **Danger** navíc kontroluje jestli jména branche, titulek pull requestu a další parametry pull requestu odpovídají standardům.

Aplikaci vyvíjíme v jazyce **[Swift](https://swift.org)**. Pro dodržování konvencí používáme **[SwiftLint](https://github.com/realm/SwiftLint)**, který kód udržuje v konzistentním stavu.

Naše aplikace jsou stavěny na architektuře **MVVM-C**, stručná dokumentace je dostupná v [iOS handbooku](https://github.com/thefuntasty/ios-handbook). Oproti MVC je přidána *view model* vrstva, která se snaží o minimalizaci controlleru a veškerá logika se děje v ní. Controller se tak stará pouze o zobrazování a zasílání eventů view modelu.

Také používáme zjednodušenné **dependency injection** pro získávání a předávání služeb – *services*. Takže dokážeme například simulovat testovací prostředí. Tento pattern se nazývá *service holder*.

Pro základní a kritické funcionality se snažíme navíc psát **unit testy**.

Na knihovny/závislosti používáme **[CocoaPods](https://github.com/CocoaPods/CocoaPods)**. Ve projektu používáme především tyto pody:

- **[FuntastyKit](https://github.com/thefuntasty/FuntastyKit)** (základy architektury MVVM, koordinátory, service holder, často používané rozšíření UIKitu)
- **[FTAPIKit](https://github.com/thefuntasty/FTAPIKit)** (deklarativní přístup k REST API)
- **[PromiseKit](https://github.com/mxcl/PromiseKit)** (funkcionální knihovna pro práci s dlouhotrvajícími tasky)

Pro distribuci provizních profilů a *Continuous Integration (CI)* používáme **Fastlane**. Služba, na které aplikace poté buildujeme a testujeme, se nazývá **Bitrise**. Každý push do *master* nebo *develop* větve pošle navíc build aplikace do *Funtasteru* (naše interní aplikace pro distribuci buildů), pro testera případně pro ostatní, co se zajímají o aktuální stav aplikace. Při vytvoření a nebo upravení pull requestu na CI proběhnou všechny testy.
