# Test Scripts  

The files in this directory are working test cases for the pyfreeipa module. Some of them do useful work.

These scripts all assume they're run from the module root directory and that the module environment is loaded, or that all the required Python modules are installed.

# The Scripts

## Working with OTP tokens

### `otptoken_find`

Prints the response of an the `otptoken_find` method

Usage:

```
python -m tests.otptoken_find [--uid <searchstring>]
```

### `otptoken_show`

Prints the response of an the `otptoken_show` method

Usage:

```
python -m tests.otptoken_find --uid <uniqueid>
```

### `update_managedby`

*WARNING* This script makes changes to the FreeIPA directroy! *WARNING*

This script requires that the account in the configuration file is either a member of the `admins` group in FreeIPA (i.e. is an Administrator), or that they are specified in the `managedBy` attributes of some/all of the otptokens in the FreeIPA directroy. If not, it will only update tokens that the configured user owns. Either use the `-f` argument to pass a configuration file with the appropriate credentials, or supply them with the `-u` and `-p` arguments.

The `update_managedby` script is idempotent and will not update tokens that already match what's defined in the configuration file.

The script checks an otptokens `managedBy` attributes against a list of proposed account UIDs and adds any UIDs from the list to the token's `managedBy` attributes, and removes any UIDs that are absent from the list.

When the dry run (`-d`) argument is used, the script summarises the state of each token found, and the prepared request that would be submitted to update them.

A normal run will summarise only those tokenas that were updated.

### Usage

To update a specific token:
```
python -m tests.update_managedby --uid <uniqueid>
```

To update all tokens the configured account can find:
```
python -m tests.update_managedby
```

### Configuration

The `update_managedby` script requires a configuration file to be created that includes the following YAML statement:

```yaml
otptoken:
  managedby:
    - tokenmanager
  ownermanagedby: True
```

### `otptoken.managedby`

This can be a single account uid, a list of account uids, or empty.

### `otptoken.ownermanagedby`

If true, a token's owner will be included as a token's manager.

## Working with user accounts

### `user_find`

### `user_show`
