--
-- PostgreSQL database dump
--

-- Dumped from database version 9.5.6
-- Dumped by pg_dump version 9.5.6

ALTER TABLE IF EXISTS ONLY public.question DROP CONSTRAINT IF EXISTS pk_question_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.answer DROP CONSTRAINT IF EXISTS pk_answer_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.answer DROP CONSTRAINT IF EXISTS fk_question_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.comment DROP CONSTRAINT IF EXISTS pk_comment_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.comment DROP CONSTRAINT IF EXISTS fk_question_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.comment DROP CONSTRAINT IF EXISTS fk_answer_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.question_tag DROP CONSTRAINT IF EXISTS pk_question_tag_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.question_tag DROP CONSTRAINT IF EXISTS fk_question_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.tag DROP CONSTRAINT IF EXISTS pk_tag_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.question_tag DROP CONSTRAINT IF EXISTS fk_tag_id CASCADE;

ALTER TABLE IF EXISTS ONLY public.user_question DROP CONSTRAINT IF EXISTS pk_user_info_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.user_question DROP CONSTRAINT IF EXISTS fk_question_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.user_answer DROP CONSTRAINT IF EXISTS pk_user_info_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.user_answer DROP CONSTRAINT IF EXISTS fk_answer_id_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.user_comment DROP CONSTRAINT IF EXISTS pk_user_info_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.user_comment DROP CONSTRAINT IF EXISTS fk_comment_id_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.user_info DROP CONSTRAINT IF EXISTS pk_user_info_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.user_question DROP CONSTRAINT IF EXISTS fk_user_info_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.user_answer DROP CONSTRAINT IF EXISTS fk_user_info_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.user_comment DROP CONSTRAINT IF EXISTS fk_user_info_id CASCADE;


DROP TABLE IF EXISTS public.question;
DROP SEQUENCE IF EXISTS public.question_id_seq;
CREATE TABLE question (
    id serial NOT NULL,
    submission_time timestamp without time zone,
    view_number integer,
    vote_number integer,
    title text,
    message text,
    image text
);

DROP TABLE IF EXISTS public.answer;
DROP SEQUENCE IF EXISTS public.answer_id_seq;
CREATE TABLE answer (
    id serial NOT NULL,
    submission_time timestamp without time zone,
    vote_number integer,
    question_id integer,
    message text,
    image text
);

DROP TABLE IF EXISTS public.comment;
DROP SEQUENCE IF EXISTS public.comment_id_seq;
CREATE TABLE comment (
    id serial NOT NULL,
    question_id integer,
    answer_id integer,
    message text,
    submission_time timestamp without time zone,
    edited_count integer
);

DROP TABLE IF EXISTS public.user_info;
DROP SEQUENCE IF EXISTS public.user_info_id_seq;
CREATE TABLE user_info (
    id serial NOT NULL,
    name text,
    password text,
    registration_date timestamp without time zone
);

DROP TABLE IF EXISTS public.user_question;
CREATE TABLE user_question (
    question_id integer NOT NULL,
    user_id integer NOT NULL
);

DROP TABLE IF EXISTS public.user_answer;
CREATE TABLE user_answer (
    answer_id integer NOT NULL,
    user_id integer NOT NULL
);

DROP TABLE IF EXISTS public.user_comment;
CREATE TABLE user_comment (
    comment_id integer NOT NULL,
    user_id integer NOT NULL
);

DROP TABLE IF EXISTS public.question_tag;
CREATE TABLE question_tag (
    question_id integer NOT NULL,
    tag_id integer NOT NULL
);

DROP TABLE IF EXISTS public.tag;
DROP SEQUENCE IF EXISTS public.tag_id_seq;
CREATE TABLE tag (
    id serial NOT NULL,
    name text
);


ALTER TABLE ONLY answer
    ADD CONSTRAINT pk_answer_id PRIMARY KEY (id);

ALTER TABLE ONLY comment
    ADD CONSTRAINT pk_comment_id PRIMARY KEY (id);

ALTER TABLE ONLY question
    ADD CONSTRAINT pk_question_id PRIMARY KEY (id);

ALTER TABLE ONLY question_tag
    ADD CONSTRAINT pk_question_tag_id PRIMARY KEY (question_id, tag_id);

ALTER TABLE ONLY tag
    ADD CONSTRAINT pk_tag_id PRIMARY KEY (id);

ALTER TABLE ONLY user_info
    ADD CONSTRAINT pk_user_info_id PRIMARY KEY (id);

ALTER TABLE ONLY user_question
    ADD CONSTRAINT pk_user_question_id PRIMARY KEY (question_id, user_id);

ALTER TABLE ONLY user_answer
    ADD CONSTRAINT pk_user_answer_id PRIMARY KEY (answer_id, user_id);

ALTER TABLE ONLY user_comment
    ADD CONSTRAINT pk_user_comment_id PRIMARY KEY (comment_id, user_id);

ALTER TABLE ONLY comment
    ADD CONSTRAINT fk_answer_id FOREIGN KEY (answer_id) REFERENCES answer(id) ON DELETE CASCADE;

ALTER TABLE ONLY answer
    ADD CONSTRAINT fk_question_id FOREIGN KEY (question_id) REFERENCES question(id) ON DELETE CASCADE;

ALTER TABLE ONLY question_tag
    ADD CONSTRAINT fk_question_id FOREIGN KEY (question_id) REFERENCES question(id) ON DELETE CASCADE;

ALTER TABLE ONLY comment
    ADD CONSTRAINT fk_question_id FOREIGN KEY (question_id) REFERENCES question(id) ON DELETE CASCADE;

ALTER TABLE ONLY user_question
    ADD CONSTRAINT fk_question_id FOREIGN KEY (question_id) REFERENCES question(id) ON DELETE CASCADE;

ALTER TABLE ONLY user_answer
    ADD CONSTRAINT fk_answer_id FOREIGN KEY (answer_id) REFERENCES answer(id) ON DELETE CASCADE;

ALTER TABLE ONLY user_comment
    ADD CONSTRAINT fk_comment_id FOREIGN KEY (comment_id) REFERENCES comment(id) ON DELETE CASCADE;

ALTER TABLE ONLY question_tag
    ADD CONSTRAINT fk_tag_id FOREIGN KEY (tag_id) REFERENCES tag(id) ON DELETE CASCADE;

ALTER TABLE ONLY user_question
    ADD CONSTRAINT fk_user_info_id FOREIGN KEY (user_id) REFERENCES user_info(id) ON DELETE CASCADE;

ALTER TABLE ONLY user_answer
    ADD CONSTRAINT fk_user_info_id FOREIGN KEY (user_id) REFERENCES user_info(id) ON DELETE CASCADE;

ALTER TABLE ONLY user_comment
    ADD CONSTRAINT fk_user_info_id FOREIGN KEY (user_id) REFERENCES user_info(id) ON DELETE CASCADE;


INSERT INTO question VALUES (0, '2017-04-28 08:29:00', 29, 7, 'How to make lists in Python?', 'I am totally new to this, any hints?', NULL);
INSERT INTO question VALUES (1, '2017-04-29 09:19:00', 15, 9, 'Wordpress loading multiple jQuery Versions', 'I developed a plugin that uses the jquery booklet plugin (http://builtbywill.com/booklet/#/) this plugin binds a function to $ so I cann call $(".myBook").booklet();

I could easy managing the loading order with wp_enqueue_script so first I load jquery then I load booklet so everything is fine.

BUT in my theme i also using jquery via webpack so the loading order is now following:

jquery
booklet
app.js (bundled file with webpack, including jquery)', 'image1.png');
INSERT INTO question VALUES (2, '2017-05-01 10:41:00', 1364, 57, 'Drawing canvas with an image picked with Cordova Camera Plugin', 'I''m getting an image from device and drawing a canvas with filters using Pixi JS. It works all well using computer to get an image. But when I''m on IOS, it throws errors such as cross origin issue, or that I''m trying to use an unknown format.
', NULL);
INSERT INTO question VALUES (3, '2017-06-23 12:29:00', 531, 102, 'How to execute large amount of sql queries asynchronous and in threads', 'Problem: I have huge amount of sql queries (around 10k-20k) and I want to run them asynchronous in 50 (or more) threads.

I wrote a powershell script for this job, but it is very slow (It took about 20 hours to execute all). Desired result is 3-4 hours max.

Question: How can I optimize this powershell script? Should I reconsider and use another technology like python or c#?

I think it''s powershell issue, because when I check with whoisactive the queries are executing fast. Creating, exiting and unloading jobs takes a lot of time, because for each thread is created separate PS instances.

My code:

$NumberOfParallerThreads = 50;


$Arr_AllQueries = @(''Exec [mystoredproc] @param1=1, @param2=2'',
                    ''Exec [mystoredproc] @param1=11, @param2=22'',
                    ''Exec [mystoredproc] @param1=111, @param2=222'')

#Creating the batches
$counter = [pscustomobject] @{ Value = 0 };
$Batches_AllQueries = $Arr_AllQueries | Group-Object -Property {
    [math]::Floor($counter.Value++ / $NumberOfParallerThreads)
};

forEach ($item in $Batches_AllQueries) {
    $tmpBatch = $item.Group;

    $tmpBatch | % {

        $ScriptBlock = {
            # accept the loop variable across the job-context barrier
            param($query)
            # Execute a command

            Try
            {
                Write-Host ""[processing ''$query'']""
                $objConnection = New-Object System.Data.SqlClient.SqlConnection;
                $objConnection.ConnectionString = ''Data Source=...'';

                $ObjCmd = New-Object System.Data.SqlClient.SqlCommand;
                $ObjCmd.CommandText = $query;
                $ObjCmd.Connection = $objConnection;
                $ObjCmd.CommandTimeout = 0;

                $objAdapter = New-Object System.Data.SqlClient.SqlDataAdapter;
                $objAdapter.SelectCommand = $ObjCmd;
                $objDataTable = New-Object System.Data.DataTable;
                $objAdapter.Fill($objDataTable)  | Out-Null;

                $objConnection.Close();
                $objConnection = $null;
            }
            Catch
            {
                $ErrorMessage = $_.Exception.Message
                $FailedItem = $_.Exception.ItemName
                Write-Host ""[Error processing: $($query)]"" -BackgroundColor Red;
                Write-Host $ErrorMessage
            }

        }

        # pass the loop variable across the job-context barrier
        Start-Job $ScriptBlock -ArgumentList $_ | Out-Null
    }

    # Wait for all to complete
    While (Get-Job -State ""Running"") { Start-Sleep 2 }

    # Display output from all jobs
    Get-Job | Receive-Job | Out-Null

    # Cleanup
    Remove-Job *

}
UPDATE:

Resources: The DB server is on a remote machine with:

24GB RAM,
8 cores,
500GB Storage,
SQL Server Management Studio (SSMS) 18.0
We want to use the maximum cpu power.

Framework limitation: The only limitation is not to use SSMS to execute the queries. The requests should come from outside source like: Powershell, C#, Python, etc.', NULL);
INSERT INTO question VALUES (4, '2018-01-13 06:45:00', 21, -21, 'Hide Location toolbar from IONIC Native InAppBrowser', 'Reading the cordova documentation inappbrowser I can not find a way to hide the Location Toolbar (ALWAYS AND WHEN it has ""location = yes"") and just for Android, becouse we can use ""toolbar=no"" on IOs.

Why the need to have active ""location = yes""? You can put ""no"" and it does not appear anymore.

As I comment in this thread, I need the activated option to be able to make use of the functions of ionic native IAB

Options i use:

location=yes,
EnableViewPortScale=yes,
hidenavigationbuttons=yes,
enableViewportScale=yes,
hideurlbar=yes,
zoom=no,
mediaPlaybackRequiresUserAction=yes,
enter image description here

As we can see in the image, the toolbar still appears at the top.

Any option that has been overlooked? Is it possible to remove it with CSS, if so, does it have any Class or ID to call, or should I touch it with pure code?', NULL);
INSERT  INTO  question VALUES (5, '2019-08-08 23:59:00', 67, -2, 'My windows seems to be outdated', 'Pls help, do I have to update Windows?', 'windows.jpg');
INSERT  INTO  question VALUES (6, '2019-08-09 10:12:00', 10, 0, 'What to do now (git)?', 'I have no idea what to do with this:', 'git.jpg');
SELECT pg_catalog.setval('question_id_seq', 6, true);

INSERT INTO answer VALUES (1, '2017-04-28 16:49:00', 4, 0, 'You need to use brackets: my_list = []', NULL);
INSERT INTO answer VALUES (2, '2017-04-25 14:42:00', 35, 0, 'Look it up in the Python docs', 'image2.jpg');
INSERT INTO answer VALUES (3, '2019-08-09 00:03:00', 60, 5, 'Rofl, put it right into the garbage and use Linux!', NULL);
INSERT INTO answer VALUES (4, '2019-08-09 00:05:00', 0, 6, 'I don''t know :(', NULL);
INSERT INTO answer VALUES (5, '2019-08-09 00:09:00', 10, 6, 'Just resolve the conflict. EZPZ', NULL);
INSERT INTO answer VALUES (6, '2019-08-09 00:18:00', 5, 6, 'Try this:', 'merge.jpg');
INSERT INTO answer VALUES (7,'2019-08-09 00:45:00', 1507, 5,'░░░░▄▄▄▄▀▀▀▀▀▀▀▀▄▄▄▄▄▄
░░░░█░░░░▒▒▒▒▒▒▒▒▒▒▒▒░░▀▀▄
░░░█░░░▒▒▒▒▒▒░░░░░░░░▒▒▒░░█
░░█░░░░░░▄██▀▄▄░░░░░▄▄▄░░░█
░▀▒▄▄▄▒░█▀▀▀▀▄▄█░░░██▄▄█░░░█
█▒█▒▄░▀▄▄▄▀░░░░░░░░█░░░▒▒▒▒▒█
█▒█░█▀▄▄░░░░░█▀░░░░▀▄░░▄▀▀▀▄▒█
░█▀▄░█▄░█▀▄▄░▀░▀▀░▄▄▀░░░░█░░█
░░█░░▀▄▀█▄▄░█▀▀▀▄▄▄▄▀▀█▀██░█
░░░█░░██░░▀█▄▄▄█▄▄█▄████░█
░░░░█░░░▀▀▄░█░░░█░███████░█
░░░░░▀▄░░░▀▀▄▄▄█▄█▄█▄█▄▀░░█
░░░░░░░▀▄▄░▒▒▒▒░░░░░░░░░░█
░░░░░░░░░░▀▀▄▄░▒▒▒▒▒▒▒▒▒▒░█
░░░░░░░░░░░░░░▀▄▄▄▄▄░░░░░█', NULL)
SELECT pg_catalog.setval('answer_id_seq', 7, true);

INSERT INTO comment VALUES (1, 0, NULL, 'Please clarify the question as it is too vague!', '2017-05-01 05:49:00');
INSERT INTO comment VALUES (2, NULL, 1, 'I think you could use my_list = list() as well.', '2017-05-02 16:55:00');
INSERT INTO comment VALUES (3, 6, NULL, 'Wow! It looks terrifying', '2019-08-09 00:11:00');
INSERT INTO comment VALUES (4, NULL, 6, 'It''s too difficult', '2019-08-09 00:20:00');
INSERT INTO comment VALUES (5, NULL, 3, 'Top comment!!!!!444', '2019-08-09 12:48:00');
SELECT pg_catalog.setval('comment_id_seq', 5, true);

INSERT INTO tag VALUES (1, 'python');
INSERT INTO tag VALUES (2, 'sql');
INSERT INTO tag VALUES (3, 'css');
SELECT pg_catalog.setval('tag_id_seq', 3, true);

INSERT INTO question_tag VALUES (0, 1);
INSERT INTO question_tag VALUES (1, 3);
INSERT INTO question_tag VALUES (2, 3);

INSERT INTO user_info VALUES (1, 'foxi', '$2b$12$xlT5IBsKlsANSQFxGV2FuumUYnZYe8QrKyZ2pqOH2VrrXO6kf1IxO','2019-08-20 12:00:04');
INSERT INTO user_info VALUES (2, 'tengely', '$2b$12$Vluf1Z165ANermX2aI8nHuipQ5qKozYQr1A.3lC.GA3PZV5nm6vz6','2019-08-20 12:00:04');
SELECT pg_catalog.setval('user_info_id_seq', 2, true);

INSERT INTO user_question VALUES (1, 1);
INSERT INTO user_answer VALUES (4, 2);
INSERT INTO user_comment VALUES (2, 1);