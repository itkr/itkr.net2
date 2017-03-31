# -*- coding: utf-8 -*-
from django.db import IntegrityError

from .entry import Entry, EntryTag, Tag


class BlogFacade(object):

    def register(self, blog_id, entry_id, title, url,
                 published, summary, summary_detail={}, tags=[]):
        """ブログのエントリー情報とタグ情報を登録する."""

        # EntryTag
        for tag in tags:
            tag = tag.term if hasattr(tag, 'term') else tag

            try:
                # 処理としては無駄なDBアクセスだけどIntegrityErrorを発生させると
                # innodbでauto_incrementが飛ぶので入れる
                EntryTag.get_by(entry_id=entry_id, name=tag)
            except EntryTag.DoesNotExist:
                EntryTag.register(entry_id=entry_id, name=tag)

        # Entry
        try:
            # 処理としては無駄なDBアクセスだけどIntegrityErrorを発生させると
            # innodbでauto_incrementが飛ぶので入れる
            Entry.get_by(entry_id=entry_id)
            return False
        except Entry.DoesNotExist:
            # ここも本当はIntegrityErroを発生させるべき
            try:
                Entry.get_by(url=url)
                return False
            except Entry.DoesNotExist:
                pass
            Entry.register(blog_id=blog_id, entry_id=entry_id,
                           title=title, url=url, published=published,
                           summary=summary, summary_detail=summary_detail)
            return True

    def create_tag_master(self):
        """EntryTag情報をもとにTagマスターを再構築する."""

        tags = [tag.name for tag in Tag.get_all()]
        for entry_tag in EntryTag.get_all():
            # 処理としては無駄なDBアクセスだけどinnodbでauto_incrementが飛ぶので入れる
            if entry_tag.name not in tags:
                try:
                    Tag.register(name=entry_tag.name)
                    tags.append(entry_tag.name)
                except IntegrityError:
                    pass

                print 'New tag:', entry_tag.name

        for tag_name in tags:
            tag = Tag.get_for_update(name=tag_name)
            tag.count = EntryTag.filter_by(name=tag_name).count()
            tag.save()
