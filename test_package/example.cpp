#include <iostream>
#include "ace/UUID.h"

int main() {
    ACE_Utils::UUID uuid;
    ACE_Utils::UUID_Generator generator;
    generator.generate_UUID(uuid);
}
