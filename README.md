# Git and Gitlab

# Зміст

* **Git**
    * **Гілки**
        * [Локальні гілки](#локальні-гілки)
        * [Віддалені гілки](#віддалені-гілки)
        * [Видалення гілок](#видалення-гілок)
        * [Злиття гілок](#злиття-гілок)
        * [Конфлікти](#конфлікти)
        * [Відновлення гілки](#відновлення-гілки)
    * **Коміти**
        * [Видалення комітів](#видалення-комітів)
        * [Вставка коміта cherry-pick](#вставка-коміта-cherry-pick)
        * [Відновлення коміта](#відновлення-коміта)
    * [**Теги**](#теги)
    * [**Ховання та чищення**](#ховання-та-чищення)
    * [**Деякі окремі команди**](#деякі-окремі-команди)
* **Gitlab**
    * **Зв'язок**
        * [Глобальні налаштування](#глобальні-налаштування)
        * [Створити новий репозиторій](#створити-новий-репозиторій)
        * [Запушити існуючу папку](#запушити-існуючу-папку)
        * [Запушити вже існуючий репозиторій](#запушити-вже-існуючий-репозиторій)
    * **Віддалені видалення**
        * [Видалення коміта](#видалення-коміта)
        * [Видалення гілок](#видалення-гілки)
    * **Обмін між репозиторіями**
        * [Процес git pull](#процес-git-pull-origin-master)
    * **[.gitignore](#gitignore)**



## Git

### Гілки

Гілки бувають **локальні** та **віддалені**, що в свою чергу діляться на *відслідковувані* та *невідслідковувані*

>**Локальні** - це гілки, які зберігаються на вашому локальному комп'ютері.

>**Віддалені** - це гілки, які зберігаються на віддаленому сховищі, наприклад, на GitHub

\
`git branch -a` - виводить список усіх локальних і віддалених гілок

`git branch -vv` - виводить список всіх локальних гілок, а також додаткову інформацію про кожну гілку. Ця інформація включає:

- Ім'я гілки

- Попередній коміт гілки

- Відслідковувана гілка

- Відставання від відслідковуваної гілки

`git branch --track [name of branch] origin [name of a tracking branch]` - встановити зв'язок, тобто утворити локально відслідковувану гілку

#### Локальні гілки

`git branch` , аналог:

`git branch -l` - виводить список тільки локальних гілок

Різниця:

| Характеристика | git branch | git branch -l |
| -------------- | ---------- | ------------- |
| Виводить всі гілки, включаючи відслідковувані віддаленим репозиторієм? | Так | Ні |
| Виводить всі гілки включаючи невідслідковувані? | Ні | Так |

#### Віддалені гілки

`git branch -r` - виводить список тільки віддалених гілок

`git ls-remote` - список всіх віддалених гілок, навіть ті, що ще пулились, тільки 
створились на гітлаб

`git branch --delete --remotes branch_name` - видалити відалену відслідковану гілку

#### Видалення гілок

`git branch -d [ім'я гілки]` - видаляє гілку тільки в тому випадку, якщо вона порожня, тобто в ній немає коммітів, які не були злиті в іншу гілку. Якщо гілка не порожня, Git видасть помилку

`git branch -d [ім'я гілки_1] [ім'я гілки_2] [ім'я гілки_3]` - видалення декількох гілок

`git branch -D [ім'я гілки] `- видаляє гілку незалежно від того, порожня вона чи ні. Якщо гілка не порожня, Git видалить усі комміти, пов'язані з цією гілкою, з локального репозиторію.

---

#### Злиття гілок

Злиття поділяється на **fast-forward** та **не fast-forward** (*recursive, ours, ....*). 

> Fast forward(швидка перемотка) - працює, якщо нема додаткових комітів 
в master після створення feature-гілки

*Merge* перемістить вказівник вперед (на останній коміт feature-гілки,
але не створить новий коміт) :

`git merge` - зміщює вказівник **HEAD** на останній коміт гілки, що зливаємо

> не Fast forward (коли з'являються додаткові коміти в гілці master після створення
feature-гілки)

*Merge* створить додатковий комміт злиття в гілці master


`git merge --no-ff feature`

або просто

`git merge` - якщо вносилися зміни у master та у feature і усе одно буде *рекурсивне*

![recursive_merge](images/recursive_merge.jpg)

Інші злиття

- `git merge --squash [name of branch]` - просто додає зміни з нової гілки у Staging Area

- `git rebase master`

Про **rebase:**

**Коли використовуємо:** 

- Під час роботи на feature-гілці з'явилися нові коміти в master-гілці і ми хочемо їх підігнати 

- feature закінчена, її реалізація повина бути додана в master-гілку без коміта злиття

**Наслідки:** Новий коміт гілки master стане батьківським комітом для комітів feature-гілки

:warning: rebase не переміщає коміти, він створює нові, не змінюйте базування комітів,
за рамками репозиторія

![rebase](images/rebase.jpg)

---

#### Конфлікти

Конфлікт можна вирішити наступними шляхами:

- Прийняти теперешні зміни (master-гілки)

- Прийняти вхідні зміни (feature-гілки)

- Прийняти обидві зміни (рядок за рядком)

- Порівняти, щоб потім обрати одне з 3 вище вказанних


`git merge --abort` - відмінити злиття

`git log --merge` - подивитися які коміти ми зливаємо

`git diff` - подивитися, де саме проблема

---

#### Відновлення гілки

1. `git reflog` - шукаємо хеш останнього коміту в гілці, яку хочемо відновити

1. `git checkout [hash of commit]` - входимо в режим зміщенного показчика

1. `git switch -c [name of branch]` - відновлення гілки

---

### Коміти

#### Видалення комітів

`git reset --hard HEAD~1` - жорстке видалення повністю; тільда значення комітів, що хочемо видалити

`git reset --soft HEAD~1` - м'яке видалення, в директорії нічого не змінюється, але коміт пропадає, в ls-files є зміни (в Staging Area). - простими словами видаляє ТІЛЬКИ коміт

`git reset HEAD~1` - файл є в робочій діректорії, коміта нема, з ls-files видаляє, показник відкатується на 1, в Staging Area - немає

---

#### Вставка коміта cherry-pick

`git cherry-pick [hash of commit]`

**Коли використовуємо:** Використовується, щоб перенести певний коміт, при цьому хеш коміта буде новий

**Приклад:** Ми допустилися помилки в гілці master. Потім створили нову гілку і почали там працювати,
змінили щось у master і потім згадали, що ми припустилися помилки, в новій гілці все виправили, за комітили і черрі-пікнули, щоб витягнути тільки ті зміни, що нам потрібні. 

:warning: ПЕРЕНОСИТЬСЯ ТІЛЬКИ ТА ЗМІНА ЯКА БУЛА СТВОРЕНА
У КОМІТІ, попередні не переносятся (тільки потрібні зміни)

---

#### Відновлення коміта

Алгортим дій:

1. `git reflog` - шукаємо хеш-коміту, що хочемо відновити

1. `git reset --hard [hash of commit]` - відновлення коміта

---

### Теги

Теги бувають **легковісні (тимчасові)** та **анотовані**.

> Легковісні - вказівник на положення коміта в гілці, приклад: гілка посилається на останній коміт

> Анотовані - повноцінні об'єкти гіт, мають інфу, приклад: email розробника створившого тег

\
`git tag` - список всіх тегів, що існують в проекті

`git tag [name of tag] [hash of commit]` - встановити тег на коміт

`git tag -a [name of tag] -m "message" [hash of commit]` - анотований тег

`git tag -d [name of tag]` - видалити тег

`git show [name of tag]` - ідображає вміст об'єкта гіт, відобразить інфу про коміт; **аналог:**

`git show [hash of commit]`

`git checkout [name of tag]` - режим зміщенного вказівника

---

### Ховання та чищення

Часто, коли ви працюєте над частиною свого проекту, усе перебуває в неохайному стані, а ви бажаєте переключити гілки щоб трохи попрацювати над чимось іншим. Складність у тому, що ви не бажаєте робити коміт напівготового завдання тільки щоб повернутися до цього стану пізніше. З цим нам допомагає команда `git stash`.

`git stash` - зберегти непідготовлені зміни і отримати до них доступ за потребою

`git stash list` - всі сховані зміни, що ми зробили

`git stash apply 1` - додати зміни у проект

`git stash push -m "message"` - повідомлення до стеш-запису

`git stash pop 0` - додати сховану зміну в проект і видалити зі стеш-листу

`git stash drop 0` - видалити останній стеш-запис

`git stash clear`- повне очищення від стеш-записів

---

### Деякі окремі команди

`git clean -df` -  видалить всі невідслідковувані файли і каталоги з робочого каталогу, включаючи файли і каталоги в підкаталогах

`git remote` - показує віддалені сервери (origin, тощо)

`git remote show origin` - детальна конфігурація гілок, проекту

`git reflog` - вказує на всі останні зміни за 14 днів, за допомогою цієї команди можна відновити
коміт або гілку

---

## Gitlab

### Зв'язок

#### Глобальні налаштування:

```
git config --global user.name "example"
git config --global user.email "example@knu.ua"
```

#### Створити новий репозиторій

```
git clone https://gitlab.com/learning9943941/l3.git
cd l3
git switch --create main
touch README.md
git add README.md
git commit -m "add README"
git push --set-upstream origin main
```

#### Запушити існуючу папку

```
cd existing_folder
git init --initial-branch=main
git remote add origin https://gitlab.com/learning9943941/l3.git
git add .
git commit -m "Initial commit"
git push --set-upstream origin main
```

#### Запушити вже існуючий репозиторій 

```
cd existing_repo
git remote rename origin old-origin
git remote add origin https://gitlab.com/learning9943941/l3.git
git push --set-upstream origin --all
git push --set-upstream origin --tags
```
___

### Віддалені видалення

#### Видалення коміта 

```
git reset --hard HEAD~1
git push --force
```

#### Видалення гілки

```
git branch -D feature
git push origin --delete feature
```

---

### Обмін між репозиторіями

Локальна гілка ->
Віддалена гілка відслідковувань (remotes/origin/master) збергіає локально зміни з віддаленої ->
Віддалена гілка ("origin" репозиторій) 

#### Процес `git pull origin master`

master(віддалена) -> (git fetch) -> remotes/origin/master -> (git merge) master (локальна)

![exchange](images/exchange.jpg)

---


### .gitignore

- `[назва файлу]`- ігнорування файлу

- `*.[розширення файлу]`- ігнорування всіх файлів з цим розширенням

- `![ім'я файлу.розширення файлу]` - крім цього файлу

- `[назва папки]/*` - назва папки і весь зміст в ній

