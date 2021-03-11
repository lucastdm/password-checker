import requests
import hashlib
import sys

def request_api_data(query_char):
	url = 'https://api.pwnedpasswords.com/range/' + query_char
	resp = requests.get(url)
	if resp.status_code != 200:
		raise RuntimeError(f'Error fetching: {resp.status_code}\n'
			'check the API and try again')
	return resp

def get_pass_leaks_count(hashes, hash_to_check):
	hashes = (line.split(':') for line in hashes.text.splitlines())
	for h, count in hashes:
		if h == hash_to_check:
			return count
	return 0

def pwned_api_check(password):
	# Check if password exists in API response
	sha1_pass = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
	first5_char, tail = sha1_pass[:5], sha1_pass[5:]
	response = request_api_data(first5_char)
	print(response)
	return get_pass_leaks_count(response, tail)

def main(args):
	for password in args:
		count = pwned_api_check(password)
		if count:
			print(f'{password} was leaked {count} times... you should probably change it.')
		else:
			print(f'{password} was not leaked yet!')

if __name__ == '__main__':
	sys.exit(main(sys.argv[1:]))