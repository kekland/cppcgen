#!/usr/bin/env dart

import 'package:ffigen/ffigen.dart';

void main(List<String> args) {
  final inputHeader = args[0];
  final outputFile = args[1];

  final generator = FfiGenerator(
    output: Output(
      dartFile: Uri.file(outputFile),
      preamble:
          '// ignore_for_file: camel_case_types, non_constant_identifier_names, unused_element, unused_field, return_of_invalid_type, void_checks, annotate_overrides, no_leading_underscores_for_local_identifiers, library_private_types_in_public_api',
      style: NativeExternalBindings(assetId: 'flmln_bindings'),
    ),
    headers: Headers(
      entryPoints: [
        Uri.file(inputHeader),
      ],
    ),
    functions: Functions(
      include: (decl) => true,
      includeSymbolAddress: (decl) => decl.originalName.contains('_destroy'),
    ),
    structs: Structs.includeAll,
    enums: Enums.includeAll,
    typedefs: Typedefs.includeAll,
    unions: Unions.includeAll,
    unnamedEnums: UnnamedEnums.includeAll,
    macros: Macros.includeAll,
    globals: Globals.includeAll,
  );

  generator.generate();
}
