# -*- coding: utf-8 -*-
"""עדכון הטקסטים הקבועים בעמוד הבסיס של אתר החומר התיאורטי, לפי חמש המצגות של הקורס.
רץ אחרי שחזור עמוד הבסיס ולפני tools/files_section.py ו-tools/units.py (ראו tools/rebuild.sh).
אפשר להריץ שוב ושוב - כל החלפה בודקת אם כבר בוצעה."""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH = os.path.join(ROOT, 'algebra-theory', 'index.html')

INTRO = ('<p>כל החומר התיאורטי של חמש המצגות - <b>מספרים מרוכבים</b>, <b>מטריצות</b>, <b>מערכות לינאריות</b>, '
         '<b>מטריצות הפיכות</b> ו<b>דטרמיננטות</b> - מסודר לפי נושאים: הגדרות, משפטים ונוסחאות, הסברים במילים, '
         'דוגמאות מחושבות והוכחות. בסוף כל חלק יש דף נוסחאות מסכם.</p>')
TAGS = ['מספרים מרוכבים', 'הצגה קוטבית', 'דה מואבר', 'מטריצות', 'כפל מטריצות', 'משוחלפת', 'עקבה',
        'מערכות לינאריות', 'דירוג וגאוס', 'מטריצה הפיכה', 'דטרמיננטה', 'קרמר']
NAV = [('#ex1', 'א. מספרים מרוכבים', 'i, פעולות, צמוד, מודול, הצגה קוטבית, דה מואבר, שורשים, משוואות ריבועיות'),
       ('#ex2', 'ב. מטריצות', 'הגדרות, סוגים, חיבור וכפל, צירוף לינארי, משוחלפת, עקבה'),
       ('#ex3', 'ג. מערכות לינאריות', 'מטריצה מורחבת, דירוג, גאוס, משתנים חופשיים, מרוכבים, פרמטר'),
       ('#ex4', 'ד. מטריצות הפיכות', 'הגדרה, תכונות, חישוב בדירוג, מטריצות אלמנטריות, פתרון מערכות'),
       ('#ex5', 'ה. דטרמיננטות', 'פיתוח, משולשת, פעולות אלמנטריות, תכונות, המטריצה הצמודה, קרמר')]


def main():
    page = open(PATH, encoding='utf-8').read()
    hero_a = page.index('<section class="hero" id="intro">')
    hero_b = page.index('</section>', hero_a)
    hero = page[hero_a:hero_b]
    hero = re.sub(r'<p>כל החומר התיאורטי של .*?</p>', INTRO, hero, count=1, flags=re.S)
    hero = re.sub(r'<div class="tags">.*?</div>', '<div class="tags">' + ''.join(f'<span>{t}</span>' for t in TAGS) + '</div>',
                  hero, count=1, flags=re.S)
    nav = '<div class="part-nav">\n' + ''.join(f'        <a href="{h}"><b>{b}</b><span>{s}</span></a>\n' for h, b, s in NAV) + '      </div>'
    hero = re.sub(r'<div class="part-nav">.*?</div>', nav, hero, count=1, flags=re.S)
    page = page[:hero_a] + hero + page[hero_b:]
    open(PATH, 'w', encoding='utf-8').write(page)
    print('theory base texts updated (5 slide decks)')


if __name__ == '__main__':
    main()
