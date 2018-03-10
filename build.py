from conan.packager import ConanMultiPackager
import copy

if __name__ == "__main__":
    builder = ConanMultiPackager()
    builder.add_common_builds(shared_option_name="ace:shared")

    items = []
    for item in builder.items:
        items.append(item)

        # create openssl variants of each build
        new_options = copy.copy(item.options)
        new_options["ace:openssl"] = True
        new_options["ace:openssl11"] = False
        items.append([item.settings, new_options, item.env_vars,
            item.build_requires, item.reference])

        new_options["ace:openssl"] = False
        new_options["ace:openssl11"] = True
        items.append([item.settings, new_options, item.env_vars,
            item.build_requires, item.reference])

    builder.items = items
    builder.run()