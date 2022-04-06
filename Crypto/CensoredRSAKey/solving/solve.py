from Crypto.Util.number import isPrime

# N = modulus
# e = public exponent
# p = one of the primes
# q = one of the primes
# d = private exponent
# dp = first exponent
# dq = second exponent
# (coefficient) qinv = ??


N = 0x00a6d26ce37013e065647e068f315881178719afb394a183ecd70d32ab63d70f2790e14d2910ef6a07e96ab69e493bae6e1e3756d9c868d934a4e09b561737246f63ebf73d235eacd31ab0893f3923ef68c4eaeac23faec3cbcf2075f22da1b56862c24158db59a8e2446bbc91146531defe8013080ce3b1519aea4e2ab93e051a76a76945dff75b01d0a556d01aad41ff28a6fdf7bdebc9f115479a7224522b1f4c3d748b806039a7680ef416b0ec78129ef5c43be20f5eac375a82aee26139375aea911a94813ab74ddbcd1de9fde490beb95cfbfe006f4c96fcc956cae566c8b9dbffcbf3648e4fff2205b664b3dd90989f5bd62f2817cb1ce01533e4199131e4142d730a3bf25c7686f30e848fd24a8cc29e1f5b79f5626bd90186848c4c3ee8d27a1d302592722f6a1885f8675e1039852317ca3b2988528bc3845f6faea673ee862222db9cc293171d809c1c7ca89747b29846c69964b2b97a31428c06f1645181e67d69501bd6c3bfdc08f63e51d922736bf84f9c1525f692f8af8819e4fd4ed8ecca302f2f9c0564bd16fabc9df0728db7acd26fc3c3bc8e9f25565044be95710a486dc79f28b234641b92b3309b3705aef60a0ead8f0eef011a0606928a06766a5da368272a67e6944485614834ed592b7d381e557b15f1c5ba12139406065784e2449e95dba762b75f6572cec479a6f65004353fd120d560c1c16fbb
e = 65537

p = 0x00d77fe12383cd9123aed6c34fa7b0d8201bc3136ac75d4d68f044a551bb2e71d13f8fcfdee1a4b1e05c3e7f79e8797ccc6e947635e2940dcda833b6b00f66011cbf7372b41f41fc67037664362e7608b1b9e3b8387ebacc1b273d257b5412f442a5f4299ead6978111a09260bb24570c960fddeca96358098941a2312331505dc2449823f6529c56c7f14d96fd45d70487db8a4b30579d7612e74cf01f3488cc28befd5af1bc4db7b79cd6c803b6bf9f5f945edec9cb4d741440f54b534a4d89d758650ef8ed0896ee099bb2a10fd1169aa00132156129679fbd0f1f9692deae73d3858a479ac78593437496314eaeb89c6b69d3bc1425e20c7dbc517f58213b7
q_upper_bits = 0x00c62c91da648462a1deb1dbcf04d0adf5dc738a8d6852a71913f27b163753512aca6836525bcee0c1607cd9fa4f20e5554284a0f7508a4cf87625450b19a288df445e5306d785eea8b56706979d7c64f31f026b01160583778cc3490b56e0174dc2b2a0b30d2ecb77e315e44b8cd607db4dcb168fd0eea97d3cefdf37b0196e20af62279232e7341063d26dd97b38a20bbc2dad33a9e0724dd42319199a889736215f60d2062fa2906c81b77d6f6c1a2a558197b196644e9659bbab86f2eda5a3f84f114fb38164317d4a14277691a0d5354dfba618868fe29793648052dec37b32

d_lower_bits = 0xa1e424dff3d5e46a0b8a1ef38a690e88280b818aeea443cbe882c8542660734c699e5cbc37e7e7c83155ea8a4e7b55bc9d243ce1a90699ab87897934eba438b43522b6d1f5f9d9ec4c05f33fe92974207677228fb940d01a1482e80bfd6290bcd07ab8b32333af5c5db61ee591904fa5f5d89733faa3cd5f2cbf7ed3a24dd104f4e0cda5a911103e0dcd2330c3ca771ef7a5f33286afdce53b15935b457ef6b8554a9775ee275db61c4f851aafd1ed90a555109b83f61f3f6b230acb42d40ad9c3f3caddc21d843308482864ac63269b84a555269b5718924606d197b3d4db6a70e8f59301

dp_lower_bits = 0xf3a5dabd

dq = 0x00c1b91607389595598939b29747acbb318984452000a83382b756256ecd3c9c2ec9586029d8677e9c6ab701dac7f96f560e455a9908d9796eb507afdbaefe8cf03c843c8386b1fd605c9c4efc6d4e09dd042637f602d1f6f729da491055a790004ae0956912ecf8a7c48c44f479c34c40dc663832f45a29c32c8b8c5882c4093cd8558a3b47996df2cbb20c023a8b5d153daa251348f008acfe40252c3b3d651bdc39c18aedd32906279c12840324d8db236520a5d04f53e773e69a41bc3e05db294419b720d1cee0f60a3173765bdbae3082800a99150998c6f5a59c2fe6658f8c5b8bda55ca94a63e81a149590e301997d74be948a6fe00ffe8a504557dcb1d

qinv = 0x00843bf5d86bfadced92a6e20f88cf104a608e8396ab17c3d9d53c229add9d59e1aeec98dd9935aef95697993241937e541db1baf42092015db549e589e58c441296546ce4c772ede517e7c7b4c133a60ff6052e1648c578daa5ef27c43ac54fe04985902680ae162dad57be7e4181d72f16ba6cbcf94413cff2d59f97cf24a8ab4bd5bd7cadc5832275eae253bab0a900bf7b826e4d8328989b13b0f413c8fd67273ad19373f92f78b921a774b07646c82e46b4c5676f611d417837797bc501e5520bc85b229f33f27d6ee48596556d69750729eb43b4f205597778a2b4b6baafe8e8e05e79eda876f08037f6ff0c437ea7f33aedeb3353f25971253fee8ebb6e

# Found using bruteforce.py
q = 25017162540548662699184632989253020378559024132253678294165804235505642778882560290161534282054571811440170071229824697771792601501274266449610508184787994190787298358977379281759347808825179985470821546624950207930247306513408985082615580895471911936426083505875368335036159328384280395436968461167910644247605943693403357148324124066256364372385768209464692266577962856109458819878197734778060533743734716991396510635123426866278260649072119529487744874492623723264069426177218753926294602524002445817596428967265366849968961700938602645329153170619352440166389324599864102348203406399240040473451906112083523824669

phi = (p-1)*(q-1)
d = pow(e,-1,phi)

# # Data recovered from the redacted PEM
# N_upper_bits = 0xa515499e52da2d53bbccd64f6eac38c5866d669c4fa50b37228dc96ae79f460f943f9c9e20d0193b085957bbe6a34ba277322dc233d754d9514e8590d55ce9ef63b127d15259c06cc705b1f40864046c8db466028b750395fc7dbaddef5c8899375bf7964e8a20e13026614d8958793b23299f2e380d4618b230d48a2c357092966a09f43c6a4400dc5932a18e05e47bb9623488bb40e16a901bcf30c33cf4f275b9577dba5e1f179ffa08012c95f098d108f45bdee04be8a136ab6f25a81c24f24f25f870e1669b6a3b3e61e350a65299776a26835c9ca92e81bbd0ba07abbcb2fe3777f44dd1f63d5dcdede9d3df754b8629d7e75e4fc107f42bac475b9567b8b89e9513ebdd715ad2fa5b922f603206cde512
# e = 65537 # assumption
# p_lower_bits = 0x77b6cb02d5f2a0aea2f9
# q = 0xc28871e8714090e0a33327b88acc57eef2eb6033ac6bc44f31baeac33cbc026c3e8bbe9e0f77c8dbc0b4bfed0273f6621d24bc1effc0b6c06427b89758f6d433a02bf996d42e1e2750738ac3b85b4a187a3bcb4124d62296cb0eecaa5b70fb84a12254b0973797a1e53829ec59f22238eab77b211664fc2fa686893dda43756c895953e573fd52aa9bb41d22306135c81174a001b32f5407d4f72d80c5de2850541de5d55c19c1f817eea994dfa534b6d941ba204b306225a9e06ddb048f4e34507540fb3f03efeb30bdd076cfa22b135c9037c9e18fe4fa70cf61cea8c002e9c85e53c1eaac935042d00697270f05b8a7976846963c933dadd527227e6c45e1
# dp = 0x878f7c1b9b19b1693c1371305f194cd08c770c8f5976b2d8e3cf769a1117080d6e90a10aef9da6eb5b34219b71f4c8e5cde3a9d36945ac507ee6dfe4c146e7458ef83fa065e3036e5fbf15597e97a7ba93a31124d97c177e68e38adc4c45858417abf8034745d6b3782a195e6dd3cf0be14f5d97247900e9aac3b2b5a89f33a3f8f71d27d670401ca185eb9c88644b7985e4d98a7da37bfffdb737e54b6e0de2004d0c8c425fb16380431d7de40540c02346c98991b748ebbc8aac73dd58de6f7ff00a302f4047020b6cd9098f6ba686994f5e043e7181edfc552e18bce42b3a42b63f7ccb7729b74e76a040055d397278cb939240f236d0a2a79757ba7a9f09
# dq_upper_bits = 1045791941318134345061297955329583824686635584654238166561681444681117346937661337003083367292099

# # derived info
# N = 0xa515499e52da2d53bbccd64f6eac38c5866d669c4fa50b37228dc96ae79f460f943f9c9e20d0193b085957bbe6a34ba277322dc233d754d9514e8590d55ce9ef63b127d15259c06cc705b1f40864046c8db466028b750395fc7dbaddef5c8899375bf7964e8a20e13026614d8958793b23299f2e380d4618b230d48a2c357092966a09f43c6a4400dc5932a18e05e47bb9623488bb40e16a901bcf30c33cf4f275b9577dba5e1f179ffa08012c95f098d108f45bdee04be8a136ab6f25a81c24f24f25f870e1669b6a3b3e61e350a65299776a26835c9ca92e81bbd0ba07abbcb2fe3777f44dd1f63d5dcdede9d3df754b8629d7e75e4fc107f42bac475b9567b8b89e9513ebdd715ad2fa5b922f603206cde512918fed2e16518cdb2f561faab195867198f4c7cd1aec3e847e010a4f0366bddbdeed9cfaf970914e98bfab41bade40972ffa13a7ad1de473acf1bbaba9c79f2827de2221b990750025082452e4a180bf2f35261519a16dffb0dbd57e39f914e62936838470924aaf2135d39e7cb938976a6781ba0c2a8e57550853a1befd7f58e5fc2e66b15821ae48caa539d64ad56080c894dbe7b93006727e94f5461fbb68853e30c270fcc2d40864a48622cae9259976be9aa1d815152f8902fda533830312fa589aebde7ae44b4fc647fe7b76c470acc701f26f72a7639d4c52f29ee13af8436d58aeccc1839a7659d9
# p = 0xd93eadbb861d5cbf29a399492c96635b5258cf51a9366b67c6692b62791c8f07a5b1cf9ba5159b3be0859791b27dae060a1cdb44658afc9a16f1e9f33fe49c269341ea21c021e97c45f85b72e02ce928b11dc88c8a199bf82a3aadd65db2936810fa31efe1e8c35170dec359ce65d45dc6aab3969211f984d70cbf89953932db56e03b499ba76013a431fc85b65364dd7c2b0a2e47e390ab886e28ee3fb5a3e4450752bbb42119de04d6269ae48b79e5586a32d86d20e6626d86c05565926ff144362c9c14e93bf746bfc50be72b0c9a51a11b929448a482053d981c102e6ca66d1d24285b851cc47017074bffdb88e252bb4978c6b177b6cb02d5f2a0aea2f9
# phi = (p-1)*(q-1)
# d = pow(e,-1,phi)

# We have found the two prime factors of the modulus
assert isPrime(p) and isPrime(q) and p*q == N

# Our private exponent matches that from dp recovered
assert d % (q-1) == dq

# The top bits of the Modulus match those recovered
#assert hex(N).startswith(hex(N_upper_bits))

# The prime p matches the low bits
assert hex(q).startswith(hex(q_upper_bits))

# The derived dq matches the recovered upper bits of dq
assert hex(d % (p-1)).endswith(hex(dp_lower_bits)[2:])