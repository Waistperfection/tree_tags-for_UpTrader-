from django.db import models
from django.db.models import F, Max, Q


class MenuItem(models.Model):
    data = models.CharField('Название категории', max_length=100)
    menu_id = models.SlugField('Имя меню', null=True, blank=True)
    left = models.IntegerField(default=1)
    right = models.IntegerField(default=2)
    parent = models.ForeignKey('self', blank=True, null=True, on_delete=models.SET_NULL)
    url_path = models.CharField('URL', max_length=200, )
    slug = models.SlugField(db_index=True, unique=True, )

    def save(self, **kwargs):
        if not self.parent:
            if self.id is None:
                left = self.__class__.objects.aggregate(left_max=Max('right'))['left_max'] or 0
                self.left = left + 1
                self.right = left + 2
        else:
            if self.id is None:
                self.left, self.right = self.parent.right, self.parent.right + 1
                query = self.__class__.objects.filter(right__gte=self.parent.right).exclude(pk=self.pk)
                for item in query:
                    item.right += 2
                    item.left = item.left + 2 if item.left >= self.right else item.left
                self.__class__.objects.bulk_update(query, fields=['right', 'left'])

        if not self.url_path:
            if not self.parent:
                self.url_path = self.slug
            else:
                self.url_path = '/'.join((self.parent.url_path, self.slug,))

        if self.parent:
            self.menu_id = self.parent.menu_id
        elif not self.menu_id:
            self.menu_id = self.slug

        super().save()

    def delete(self, **kwargs):
        left, right = self.left, self.right
        correction = right-left+1
        del_query = self.__class__.objects.filter(Q(left__gte=left) & Q(right__lte=right))
        upd_query = self.__class__.objects.filter(right__gt=right)

        for item in upd_query:
            item.left = item.left if item.left < left else item.left-correction
            item.right -= correction

        del_query.delete()
        self.__class__.objects.bulk_update(upd_query, fields=['right', 'left'])
        super().delete()

    def get_branch(self):
        if self.parent_id:
            query = self.__class__.objects.filter(
                Q(parent_id=self.id) |
                Q(pk=self.pk) |
                Q(right__gt=self.right) & Q(left__lt=self.left)
            )
        else:
            query = self.__class__.objects.filter(
                Q(parent_id=self.id)|
                Q(pk=self.pk)
            )

        return query

    class Meta:

        ordering = ['left']

    def __str__(self):
        return '-'*(len(self.url_path.split('/'))-1) + self.data
