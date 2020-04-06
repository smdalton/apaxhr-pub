from users import admin

permissions_groups = {
    # access to only their own documents and Employee Profile info
    'tier1': [
        'Applicants',
        'Trainees',
        'Teachers', ],
    # Access to centers, rooms, classes, and
    'tier2': [
        'Head Teachers',
        'Faculty Managers',
    ],
    # Acess to modify employee placements (move employees to new positions)
    'tier3': [
        'Area Managers',
        'HR Managers',
    ],
    'tier4': [
        'Teacher Management Directors',
        'Training Directors',
        'Recruiting Directors',
    ],
    # Access to modify permissions, payroll data, employee positions
    'tier5': [
        'HR Directors',
        # this one is just for development
        'Developers'
    ]
}


def get_all_permissions_groups():
    return [item for sublist in permissions_groups.values() for item in sublist]




class DefaultPermissionsMixin(admin.ModelAdmin):
    perms_list = ['Applicants','Trainees', 'Teachers']

    def has_module_permission(self, request, obj=None):
        perms = list(request.user.groups.values_list('name', flat=True))
        if any(item in self.perms_list for item in perms):
            print('has change permission')
            return True
        else:
            return False