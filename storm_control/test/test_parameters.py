#!/usr/bin/env python
"""
Tests of the parameters object functionality.
"""

import storm_control.test as test

import storm_control.sc_library.parameters as params


def test_parameters_1():

    # Load parameters.
    p1 = params.parameters(test.xmlFilePathAndName("test_parameters.xml"), recurse = True)
    
    # Check a parameter.
    assert (p1.get("camera1.flip_horizontal") == False)

    # Change it's value.
    p1.set("camera1.flip_horizontal", True)

    # Check again.
    assert (p1.get("camera1.flip_horizontal") == True)


def test_parameters_2():

    # Load parameters.
    p1 = params.parameters(test.xmlFilePathAndName("test_parameters.xml"), recurse = True)

    # Copy.
    p2 = p1.copy()

    # Check that p1 and p2 store the same values and have
    # the same structure.
    assert (len(params.difference(p1, p2)) == 0)

    # Change a value in p2.
    p2.set("camera1.flip_horizontal", True)

    # Check that p1 is still the same.
    assert (p1.get("camera1.flip_horizontal") == False)

    # Get the difference between p1 and p2.
    assert (params.difference(p1, p2)[0] == 'camera1.flip_horizontal')
    

def test_parameters_3():

    # Load parameters.
    p1 = params.parameters(test.xmlFilePathAndName("test_parameters.xml"), recurse = True)

    # Test sub-section creation.
    p2 = params.StormXMLObject()
    p2s = p2.addSubSection("camera1", p1.get("camera1").copy())
    p2s.add(params.ParameterInt(name = "test", value = 5))

    # p2 is different then p1 because it has 'test'.
    assert (params.difference(p2.get("camera1"), p1.get("camera1"))[0] == "test")

    # But p1 is not different from p2 because difference() only
    # checks p1 properties that exist in p1.
    assert (len(params.difference(p1.get("camera1"), p2.get("camera1"))) == 0)
    

def test_parameters_4():

    # Load parameters.
    p1 = params.parameters(test.xmlFilePathAndName("test_parameters.xml"), recurse = True)

    # Create another set of parameters with only 1 item.
    p2 = params.StormXMLObject()
    p2.add(params.ParameterString(name = "test_param", value = "bar"))
    p2s = p2.addSubSection("camera1")
    p2s.add(params.ParameterSetBoolean(name = "flip_horizontal", value = True))
    p2s.add(params.ParameterSetBoolean(name = "flip_vertical", value = False))

    # Test copy.
    [p3, ur] = params.copyParameters(p1, p2)

    # Their should be one un-recognized parameter, 'flip_vertical'.
    assert (len(ur) == 1) and (ur[0] == "flip_vertical")

    # 'camera1.flip_horizontal' in p3 should be True.
    assert p3.get("camera1.flip_horizontal")

    # 'test_param' should be 'bar'.
    assert (p3.get("test_param") == "bar")


def test_parameters_5():

    # Load parameters.
    p1 = params.parameters(test.xmlFilePathAndName("test_parameters.xml"),
                           recurse = True,
                           add_filename_param = False)

    # Save.
    p1.saveToFile("temp.xml")

    # Re-load.
    p2 = params.parameters("temp.xml",
                           recurse = True,
                           add_filename_param = False)

    # Check that they are the same.
    assert (len(params.difference(p1, p2)) == 0) and (len(params.difference(p2, p1)) == 0)

    
if (__name__ == "__main__"):
    test_parameters_1()
    test_parameters_2()
    test_parameters_3()
    test_parameters_4()
    test_parameters_5()
