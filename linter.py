from SublimeLinter.lint import NodeLinter


class Tsc(NodeLinter):
    name = 'tsc-lint'
    """
    Use tsc compiler to bulid .ts, .tsx files.
    https://www.typescriptlang.org/docs/handbook/compiler-options.html

    --noEmit option: Disable emitting files from a compilation.
    --skipLibCheck option: Disable check *.d.ts files.
    """
    cmd = 'tsc --noEmit --pretty true --skipLibCheck true ${file}'

    """
    The output of tsc like this:
    "index.ts:8:3 - error TS2322: Type 'string' is not assignable to type 'number'."

    By the way, there is another format if you run tsc with "--pretty false":
    "index.ts(8,3): error TS2322: Type 'string' is not assignable to type 'number'."
    """
    regex = (r'^(?P<filepath>(.*)):(?P<line>\d+):(?P<col>\d+)\s-\s(?P<error>error(.*)):\s(?P<message>(.*$))')
    defaults = {
        'selector': 'source.ts, source.tsx'
    }

    def split_match(self, match):
        """
        Filter extraneous files.
        tsc output all errors that from other dependent files.

        See https://github.com/SublimeLinter/SublimeLinter/issues/1238
        """
        tmp = super().split_match(match)

        filename = match.group('filepath').replace('/', '\\')
        fullpath = self.view.file_name()

        if fullpath and filename and fullpath.endswith(filename):
            return tmp

        return None


# class VueTsc(NodeLinter):
#     name = 'vue-tsc-lint'
#     """
#     Use vue-tsc compiler to build .vue files.
#     https://github.com/johnsoncodehk/volar/tree/master/packages/vue-tsc
#         if fullpath and filename and fullpath.endswith(filename):
#             return tmp

#     NOT SUPPORT vue 2.x
#     vue-tsc only supports vue 3.x, does not support vue 2.x
#     https://github.com/vuejs/vue-cli/issues/5192
#     """
#     cmd = 'vue-tsc --noEmit --pretty true --skipLibCheck true ${file}'
#     regex = (r'^(?P<filepath>(.*)):(?P<line>\d+):(?P<col>\d+)\s-\s(?P<error>error(.*)):\s(?P<message>(.*$))')
#     defaults = {
#         'selector': 'text.html.vue, source.ts.embedded.html'
#     }
