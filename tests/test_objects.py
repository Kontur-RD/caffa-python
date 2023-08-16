import logging
import sys
import pytest
import caffa
import json

log = logging.getLogger("test_objects")


class TestObjects(object):
    def setup_method(self, method):
        self.testApp = caffa.Client("localhost", 50000)

    def teardown_method(self, method):
        self.testApp.cleanup()

    def test_document(self):
        doc = self.testApp.document("testDocument")
        assert doc is not None
        print(str(doc))
        print("Found document: " + doc.keyword)
        print("With schema: " + json.dumps(self.testApp.schema(doc.keyword)))

    def test_fields(self):
        doc = self.testApp.document("testDocument")
        print(doc)
        assert doc is not None
        keywords = dir(doc)
        assert len(keywords) > 0
        for keyword in keywords:
            print("Found field: " + keyword)

        print("Found filename: " + doc.fileName)
        assert doc.fileName == "dummyFileName"
        try:
            doc.fileName = "TestValue"
        except Exception as e:
            pytest.fail("Failed with exception {0}", e)
        assert doc.fileName == "TestValue"
        doc.fileName = "dummyFileName"


    def test_children(self):
        return

        doc = self.testApp.document("testDocument")
        assert doc is not None
        keywords = vars(doc)
        assert "demoObject" in keywords
        demo_object = doc.demoObject
        assert demo_object is not None
        log.debug("Found demo object: %s", str(demo_object))

    def test_methods(self):
        doc = self.testApp.document("testDocument")
        assert doc is not None
        
        demo_object = doc.demoObject
        assert demo_object is not None
        obj_methods = demo_object.methods()
        assert len(obj_methods) > 0

        for method in obj_methods:
            print("Found method: ", method.name(), dir(method))
        
        demo_object.copyValues.execute(intValue = 41, doubleValue = 99.0, stringValue = "AnotherValue")

        assert demo_object.doubleField == 99.0
        assert demo_object.intField == 41
        assert demo_object.stringField == "AnotherValue"

        demo_object.copyValues.execute(42, 97.0, "AnotherValue2")

        assert demo_object.doubleField == 97.0
        assert demo_object.intField == 42
        assert demo_object.stringField == "AnotherValue2"

        demo_object.setIntVector.execute(intVector = [1, 2, 97])

        assert demo_object.get("proxyIntVector") == [1, 2, 97]

        values = demo_object.getIntVector.execute()

        assert(values == [1, 2, 97])

    def test_non_existing_field(self):
        doc = self.testApp.document("testDocument")
        assert doc is not None
        try:
            value = doc.does_not_exist
            pytest.fail("Should have had exception, but got none!")
        except Exception as e:
            log.info(
                "Got expected exception when trying to read a field which doesn't exist: '{0}'".format(e))

    def test_int_vector(self):
        doc = self.testApp.document("testDocument")
        assert doc is not None

        demo_object = doc.get("demoObject")
        demo_object.set("proxyIntVector", [1, 4, 42])
        assert demo_object.get("proxyIntVector") == [1, 4, 42]

    def test_float_vector(self):
        doc = self.testApp.document("testDocument")
        assert doc is not None

        demo_object = doc.get("demoObject")
        demo_object.floatVector = [1.0, 3.0, -42.0]
        assert demo_object.floatVector == [1.0, 3.0, -42.0]

    def test_app_enum(self):
        doc = self.testApp.document("testDocument")
        assert doc is not None
        demo_object = doc.get("demoObject")
        demo_object.set("enumField", "T3")
        assert demo_object.get("enumField") == "T3"

        try:
            demo_object.set("enumField", "InvalidValue")
            pytest.fail("Should have failed to set invalid value")

        except Exception as e:
            log.info(
                "Got expected exception when trying to assign an invalid enum value: '0'".format(e))
