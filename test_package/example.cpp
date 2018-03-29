#include <iostream>
#include "ace/UUID.h"

int ACE_TMAIN (int argc, ACE_TCHAR *argv[]) {
    ACE_Utils::UUID uuid;
    ACE_Utils::UUID_Generator generator;
    generator.generate_UUID(uuid);
    return 0;
}
