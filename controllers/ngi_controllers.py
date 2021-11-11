from models import Chapter


class ChapterController:
    def __init__(self):
        pass

    def add(self, chapter):
        existing = Chapterchapters.query.filter_by(name=chapter['name']).first()
        if not existing:
            new_chapter.name = chapter['name']
            new_chapter.founder = chapter['founder']
            new_chapter.founded = chapter['founded']
            db.session.add(new_chapter)
            db.session.commit()
            return True

        return False

    def edit(self, chapter):
        existing_chapter = Chapterchapters.query.filter_by(id=chapter['id']).first()
        if existing_chapter:
            existing_chapter.name = chapter['name']
            existing_chapter.founder = chapter['founder']
            existing_chapter.founded = chapter['founded']
            db.session.commit()
            return True

        return False

    def delete(self, chapter):
        existing_chapter = Chapterchapters.query.filter_by(id=chapter['id']).first()
        if existing_chapter:
            db.session.delete(existing_chapter)
            db.session.commit()
            return True

        return False