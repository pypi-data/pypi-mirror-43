<html>
<head>
	<title>Login page</title>
	<link rel="stylesheet" href="${request.static_url('ppss_auth:ppss_auth_static/ppssauth.css')}" type="text/css" />
	<%block name="ppssautcss">

	</%block>
</head>
<body class="ppss_auth">
${next.body()}
</body>

</html>