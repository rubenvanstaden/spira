import spira.all as spira


cnt = 0
class MyClass(spira.FieldInitializer):

    prop_a = spira.StringField(default='a')
    prop_aa = spira.DataField(fdef_name='create_prop_aa')

    def create_prop_aa(self):
      global cnt
      cnt = cnt + 1
      print("called '_default_prop_aa' {} times".format(cnt))
      return self.prop_a * 2


my_cls = MyClass()
my_cls.prop_aa



