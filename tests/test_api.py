class APITestCase(unittest.TestCase):

    #.....
    def get_api_headers(self, username, password):
        return {
            'Authorization':
            'Basic' + b64encode((username+':'+password).encode('utf-8')).decode('utf-8'),
            'Accept': 'application/json',
            'Content-Type': 'applciation/json'
            }
    def test_no_auth(self):
        response = self.client.get(url_for('api.get_posts'),
                                   content_type='application/json')
        self.assertTrue(response.status_code == 401)

    def test_posts(self):

        #add a user
        r = Role.query.filter_by(name='User').first()
        self.assertIsNotNone(r)
        u = User(email='john@example.com', password='cat', confirmed=True,
                 role=r)
        db.session.add(u)
        db.session.commit()


        #write a post
        response = self.client.post(
            url_for('api.new_post'),
            headers = self.get_auth_header('john@example.com', 'cat'),
            data = jaon.dumps({'body': 'body of the blog post'}))
        self.assertTrue(response.status_code == 201)
        url = response.headers.get('Location')
        self.assertIsNotNone(url)

        #get the new post
        response = self.client.get(url,
                                   headers= self.get_auth_header('john@example.com','cat'))


        self.assertTrue(reposnse.status_code == 200)
        json_reponse = json.loads(response.data.decode('utf-8'))
        self.assertTrue(json_response['url'] == url)
        self.assertTrue(json_response['body'] == 'body of the *blog* post')
        self.assertTrue(json_response['body_html'] == '<p>Body of the <em> blog</em> post</p>')
