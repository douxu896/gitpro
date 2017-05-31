package dou;

import java.io.File;
import java.util.Iterator;
import java.util.List;

import org.dom4j.Attribute;
import org.dom4j.Document;
import org.dom4j.DocumentException;
import org.dom4j.Element;
import org.dom4j.io.SAXReader;

public class Dom {

	public static void main(String[] args) throws DocumentException {
		// TODO Auto-generated method stub
	    SAXReader reader = new SAXReader();  
	    reader.setEntityResolver(new IgnoreDTDEntityResolver());   
        String path = "/home/emily/Desktop/Xmldata/PMC/Adm_Policy_Ment_Health/Adm_Policy_Ment_Health_2010_Mar_15_37(1-2)_201-204.nxml";
        Document document = reader.read(new File(path));

        // 获取根元素
        Element root = document.getRootElement();
        System.out.println("Root: " + root.getName());
        System.out.println("-------获取属性前------");  
        //获取节点student1  
        Element abstractElement = root.element("abstract");  
        //遍历  
        //listNodes(abstractElement);  
        //获取其内容  
     String abstracttext = abstractElement.getText();
     System.out.println(abstracttext);
        System.out.println("-------获取属性后------");  
       
	}

	private static void listNodes(Element node) {
		// TODO Auto-generated method stub
		 System.out.println("当前节点的名称：" + node.getName());  
	        //首先获取当前节点的所有属性节点  
	        List<Attribute> list = node.attributes();  
	        //遍历属性节点  
	        for(Attribute attribute : list){  
	            System.out.println("属性"+attribute.getName() +":" + attribute.getValue());  
	        }  
	        //如果当前节点内容不为空，则输出  
	        if(!(node.getTextTrim().equals(""))){  
	             System.out.println( node.getName() + "：" + node.getText());    
	        }  
	        //同时迭代当前节点下面的所有子节点  
	        //使用递归  
	        Iterator<Element> iterator = node.elementIterator();  
	        while(iterator.hasNext()){  
	            Element e = iterator.next();  
	            listNodes(e);  
	        }  
	    }  
	}


