#include <iostream>
#include "ace/UUID.h"

#if defined WITH_SSL
#include "ace/SSL/SSL_Context.h"
#endif

int ACE_TMAIN (int argc, ACE_TCHAR *argv[]) {
    ACE_Utils::UUID uuid;
    ACE_Utils::UUID_Generator generator;
    generator.generate_UUID(uuid);

#if defined WITH_SSL
    ACE_SSL_Context context;
    context.set_mode();
#endif

    return 0;
}
