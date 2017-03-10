# External run Let’s encrypt/acme role for Ansible

[![Build Status](https://travis-ci.org/morbidick/ansible-role-letsencrypt.svg?branch=master)](https://travis-ci.org/morbidick/ansible-role-letsencrypt)

This role should be run periodically (for example with [ansible tower](https://www.ansible.com/tower) or [rundeck](http://rundeck.org/)) to renew certificates. For now only the http-01 challenge is supported (maybe you wanna write a PR? ;) ).

It automates the following tasks:

  * creating an account key for Let’s encrypt
  * creating private keys and Certificate Signature Requests (CSR) for hosts
  * renew certificates
  * trigger service reload

## Requirements

For every hostname you want to support, you need to have a webserver configured and add an alias that points to the
directory configured with `letsencrypt_challenges_directory`. For Apache, such an alias should look like this:

````
Alias "/.well-known/acme-challenge" "{{ letsencrypt_challenges_directory }}"
````

Hint: You can also put this into a global variable and then use this variable in the definition of every vHost.

## Role Variables

You might want to adjust some variables, especially where the challenges are located.

* `letsencrypt_challenges_directory`: The (web-reachable) directory that contains the temporary challenges used for
verifying your domain ownership
* `letsencrypt_intermediate_cert_path`: the path to which the intermediate certificate of Let’s encrypt will be
downloaded.
* `letsencrypt_account_key_source_file`: the path to the local account key file to copy over to the server. Leave this variable undefined to let this role generate the account key.
* `letsencrypt_account_key_source_contents`: the actual content of the key file including the BEGIN and END headers. Leave this variable undefined to let this role generate the account key.
* `letsencrypt_account_mail`: the mail address to update your account to
* `letsencrypt_reload_services`: a list of services that need to be reloaded on certificate update.

Add the certificates to generate to their respective hosts (important! if the certificate is not generated on the host the DNS A record points to, Let’s encrypt won’t be able to verify if the hostname really belongs to you and thus won’t give you the certificate!):

````
letsencrypt_certs:
- host: "myhost.example.com"
- host:
  - "foo.example.org"
  - "bar.example.org"
- name: webservers
  - "www1.example.org"
  - "www2.example.org"
````

The certificate will be placed at `{{ letsencrypt_certs_dir }}/{{ name }}.crt`, if no name is given it will be named after the first host.
The key is placed at `{{ letsencrypt_keys_dir }}/{{ name }}.key`.
Other optoinal options are:
- `name`: defaults to the first given host
- `challenge_type`:: which challenge type should be used, defaults `letsencrypt_default_challenge_type` - http-01

For multidomain certificates, all mentioned names must point to the server where the certificate is being generated.

You can optionally also set the permissions of the key and cert, with these options which are fed in to Ansible’s file module:
- `key_owner`: a user name, e.g. root or www-data
- `key_group`: a group name, e.g. root or ssl-certs or www-data
- `key_permissions`: an octal mode, like "0600". This must be specified as a quoted string. Without the quotes, it did
not work for me (read: the number was interpreted as octal and converted to decimal)
- `cert_owner`
- `cert_group`
- `cert_permissions`

The default mode is root/root/0600 and root/root/0750, i.e. the file is only read-/writable by root. Make sure you never make the key world-readable! If you do, everybody with shell access to the server might be able to compromise your encrypted connections. You can also change the defaults by setting these variables:

- `letsencrypt_default_key_owner`
- `letsencrypt_default_key_group`
- `letsencrypt_default_key_permissions`
- `letsencrypt_default_cert_owner`
- `letsencrypt_default_cert_group`
- `letsencrypt_default_cert_permissions`

For more options see [defaults/main.yml](defaults/main.yml)

## Certificate chain

The intermediate certificate of Let’s encrypt is downloaded to `letsencrypt_intermediate_cert_path`. You should include
it in the webserver config to have it delivered to visitors.

## Reusing existing account keys

When you use Let's encrypt on multiple servers, it may be simpler to have only one account defined with Let's encrypt. You can do that with this role by proceeding as follow:

1. Run the role on a first server, a new account.key file is created for you.
2. Register the account public key with Letsencrypt using for example [Gethttpsforfree](https://gethttpsforfree.com/)
3. Copy /etc/ssl/letsencrypt/keys/letsencrypt_account.key from the first server to your computer
4. Recommended: secure the account.key file. It should never be accessible to anybody otherwise the security of your site may be compromised as an attacker may impersonate you.
5. For new servers, setup `letsencrypt_account_key_source` to point to the local account.key file. The file account.key will be copied to the server and you will be able to reuse the same account with Letencrypt for all your servers.

## Dependencies

No direct dependencies, but of course you will need to have a webserver configured (e.g. Apache); this role does not support setting up a temporary server.

## Development

You can use the Vagrantfile for local testing, just install vagrant and virtualbox and execute the following commands:

````
vagrant up
vagrant provision
````

## TODO

This role is brand-new, so it needs testing. I tested it on Ubuntu, where it works fine, but YMMV. If you can get it to run on other systems, I’d be happy to hear about that. I’m also happy if you report any issues you run into.

  * implement other challenges
  * reimplement chained certs
  * cleanup old certs

## License

MIT


## Author Information

Forked and ported to Ansibles Let's encrypt module by [morbidick](https://github.com/morbidick/).

The original acme-tiny role was created by Andreas Wolf. Visit his [website](http://a-w.io) and [Github profile](https://github.com/andreaswolf/) or follow him on [Twitter](https://twitter.com/andreaswo).

### Contributors

*(in alphabetic order)*

  * [Ludovic Claude](https://github.com/ludovicc)
  * [tgagor](https://github.com/tgagor)
